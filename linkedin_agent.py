import tkinter as tk
import threading
import time
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import base64
import io
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tkinter import ttk

def generate_qr_image(driver, qr_label):
    """
    WhatsApp Web'in QR kodunu yakalar ve GUI'de görüntüler.
    """
    # WhatsApp Web'e bağlan
    driver.get("https://web.whatsapp.com/")
    time.sleep(5)  # QR kodu yüklenmesi için bekleme

    # QR kod elementini bul
    try:
        qr_element = driver.find_element(By.CSS_SELECTOR, "canvas[aria-label='Scan this QR code to link a device!']")
        qr_base64 = qr_element.screenshot_as_base64

        # Base64 string'ini binary veriye dönüştürme
        qr_data = base64.b64decode(qr_base64)
        image = Image.open(io.BytesIO(qr_data))

        # QR resmini GUI'ye ekleme
        qr_photo = ImageTk.PhotoImage(image)
        qr_label.config(image=qr_photo)
        qr_label.image = qr_photo
    except Exception as e:
        qr_label.config(text=f"QR kod alınamadı: {e}", fg="red")

def select_chat(driver, chat_name, status_label):
    """
    Sohbet listesindeki belirtilen sohbeti seçer ve GUI'ye durumu yazdırır.
    """
    try:
        chats = driver.find_elements(By.XPATH, "//span[@dir='auto']")
        for chat in chats:
            if chat.text == chat_name:
                chat.click()
                time.sleep(3)
                status_label.config(text=f"Sohbete girildi: {chat_name}")
                return True
        status_label.config(text=f"Sohbet bulunamadı: {chat_name}", fg="red")
        return False
    except Exception as e:
        status_label.config(text=f"Hata: {e}", fg="red")
        return False

def process_messages(driver, status_label, processed_links, email):
    """
    Sohbetten gelen mesajları kontrol eder, LinkedIn bağlantılarını işler ve GUI'yi günceller.
    """
    try:
        messages = driver.find_elements(By.CSS_SELECTOR, "span.selectable-text.copyable-text")
        
        for message in messages:
            text = message.text
            linkedin_links = re.findall(r'https://www\.linkedin\.com/in/\S+', text)
            for link in linkedin_links:
                if link not in processed_links:
                    processed_links.add(link)
                    status_label.config(text=f"Yeni LinkedIn bağlantısı bulundu: {link}", fg="green")
                    # LinkedIn'e gidip bağlantı isteği gönderme
                    send_connection_request(driver, link, email, status_label)
                    time.sleep(2)  # Bağlantı isteği gönderildikten sonra biraz bekle
    except Exception as e:
        status_label.config(text=f"Mesaj kontrol edilirken hata: {e}", fg="red")
        
def start_process(email, password, status_label, qr_label):
    """
    Programı başlatan ve WhatsApp Web'e bağlanan fonksiyon.
    """
    status_label.config(text="LinkedIn'e giriş yapılıyor...")
    
    # Headless mod için seçenekler oluştur
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # LinkedIn'e giriş yap
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        driver.find_element(By.ID, "username").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)  # LinkedIn'e giriş yapılmasını bekle

        status_label.config(text="WhatsApp'a bağlanıyor...")

        # WhatsApp QR kodu gösterme
        generate_qr_image(driver, qr_label)
        time.sleep(35)

        # WhatsApp'a bağlandıktan sonra sohbet seçmeye başla
        chat_name = "Yapay Zeka Fabrikası"  # Sohbet adı
        if select_chat(driver, chat_name, status_label):
            status_label.config(text="Sohbet dinleniyor...")

            processed_links = set()  # LinkedIn bağlantılarını takip etmek için set
            while True:
                # Yeni gelen mesajları kontrol et
                process_messages(driver, status_label, processed_links, email)

                time.sleep(5)  # 5 saniyede bir yeni mesajları kontrol et
    finally:
        driver.quit()
        
def start_in_thread(email, password, status_label, qr_label):
    """
    Start process'ini arka planda çalıştırmak için thread oluşturuyoruz.
    """
    threading.Thread(target=start_process, args=(email, password, status_label, qr_label), daemon=True).start()

    
def check_whatsapp_messages(driver, processed_links, status_label):
    """
    WhatsApp'tan mesajları okur ve LinkedIn linklerini bulur.
    """
    try:
        messages = driver.find_elements(By.CSS_SELECTOR, "span.selectable-text.copyable-text")
        linkedin_links = []

        for message in messages:
            text = message.text
            links = re.findall(r'https://www\.linkedin\.com/in/\S+', text)  # LinkedIn linklerini bul
            for link in links:
                if link not in processed_links:
                    linkedin_links.append(link)
                    processed_links.add(link)

        return linkedin_links
    except Exception as e:
        status_label.config(text=f"Mesaj kontrol edilirken hata: {e}", fg="red")
        return []


def send_connection_request(driver, profile_url, email, status_label):
    connection_sent = False
    driver.execute_script(f"window.open('{profile_url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])

    try:
        wait = WebDriverWait(driver, 15)
        div = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "QfXyyPtXfkPxedYpDVSyjhQGQnDl")
        ))

        first_button = div.find_elements(By.TAG_NAME, "button")[0]
        first_button_aria_label = first_button.get_attribute("aria-label")

        if "adlı kullanıcıyı bağlantı kurmak için davet et" in first_button_aria_label:
            driver.execute_script("arguments[0].click();", first_button)
            send_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='Not olmadan gönderin']")
            ))
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", send_button)
            driver.execute_script("arguments[0].click();", send_button)
            connection_sent = True
            time.sleep(2)
            return

        elif "adlı kullanıcıyı takip et" in first_button_aria_label:
            second_button = div.find_elements(By.TAG_NAME, "button")[1]
            second_button_aria_label = second_button.get_attribute("aria-label")

            if "adlı kullanıcıyı bağlantı kurmak için davet et" in second_button_aria_label:
                driver.execute_script("arguments[0].click();", second_button)
                time.sleep(2)
                
                try:
                    email_input = driver.find_element(By.CSS_SELECTOR, "input.ember-text-field.ember-view.mb3")
                    email_input.send_keys(email)
                    connection_sent = True
                except Exception:
                    pass

                send_button = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Not olmadan gönderin']")
                ))
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", send_button)
                driver.execute_script("arguments[0].click();", send_button)
                connection_sent = True
                time.sleep(2)
                return

        more_actions_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Daha fazla işlem']")))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", more_actions_button)
        driver.execute_script("arguments[0].click();", more_actions_button)

        connect_button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='display-flex t-normal flex-1' and text()='Bağlantı kur']")))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", connect_button)
        driver.execute_script("arguments[0].click();", connect_button)

        time.sleep(2)
        try:
            email_input = driver.find_element(By.CSS_SELECTOR, "input.ember-text-field.ember-view.mb3")
            email_input.send_keys(email)
            connection_sent = True
        except Exception:
            pass

        send_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Not olmadan gönderin']")))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", send_button)
        driver.execute_script("arguments[0].click();", send_button)
        connection_sent = True
        time.sleep(2)

    except Exception as e:
        pass
    finally:
        if not connection_sent:
            try:
                profile_name = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").text
                status_label.config(
                    text=f"Uyarı: {profile_name} profiline bağlantı isteği gönderilemedi.\nBu profil ile daha önce bağlantı kurulmuş olabilir.",
                    fg="orange"
                )
            except:
                status_label.config(
                    text=f"Uyarı: Profil bağlantısına istek gönderilemedi.\nBu profil ile daha önce bağlantı kurulmuş olabilir.",
                    fg="orange"
                )
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def create_gui():
    root = tk.Tk()
    root.title("LinkedIn Bağlantı Gönderici")
    root.geometry("600x700")
    root.resizable(False, False)
    
    # Ana container frame (artık direkt root'a bağlı)
    main_container = tk.Frame(root)
    main_container.pack(fill=tk.BOTH, expand=True)
    
    # Ana başlık
    header_frame = tk.Frame(main_container, bg="#0077B5", width=600, height=60)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text="WhatsApp-LinkedIn Entegrasyonu",
        font=("Arial", 16, "bold"),
        bg="#0077B5",
        fg="white"
    )
    title_label.pack(pady=15)
    
    # Geliştirici bilgisi
    developer_frame = tk.Frame(main_container, bg="#f0f0f0", width=600, height=40)
    developer_frame.pack(fill=tk.X)
    developer_frame.pack_propagate(False)
    
    developer_label = tk.Label(
        developer_frame,
        text="Geliştirici: Tamer Kanak (tamerkanak75@gmail.com)",
        font=("Arial", 9),
        bg="#f0f0f0"
    )
    developer_label.pack(pady=10)
    
    # Scrollable canvas
    canvas = tk.Canvas(main_container)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Sohbet adı girişi
    chat_input_frame = tk.Frame(scrollable_frame)
    chat_input_frame.pack(pady=10)

    tk.Label(
        chat_input_frame,
        text="Hangi sohbetten LinkedIn profillerini çekmek istiyorsanız sohbetin adını girin:",
        font=("Arial", 10, "bold"),
        wraplength=500,
        justify="left"
    ).pack(pady=5)

    chat_name_entry = tk.Entry(chat_input_frame, width=40)
    chat_name_entry.pack(pady=5)

    # Sohbet adı kaydetme butonu
    def set_chat_name():
        chat_name = chat_name_entry.get()
        if chat_name:
            status_label.config(text=f"Dinlenecek sohbet: {chat_name}", fg="green")
            return chat_name
        else:
            status_label.config(text="Lütfen bir sohbet adı girin.", fg="red")
            return None

    chat_name_button = tk.Button(
        chat_input_frame,
        text="Sohbet Adını Ayarla",
        font=("Arial", 10, "bold"),
        bg="#00a650",
        fg="white",
        width=20,
        command=set_chat_name
    )
    chat_name_button.pack(pady=10)
    
    # Açıklama metni
    description_text = """
    Bu uygulama WhatsApp üzerinden gelen LinkedIn profillerini otomatik olarak
    bağlantı isteği göndermek için tasarlanmıştır.
    
    Kullanım Adımları:
    1. LinkedIn hesap bilgilerinizi girin
    2. 'Başlat' butonuna tıklayın
    3. Görüntülenen QR kodu WhatsApp Web'de okutun
    4. Program otomatik olarak mesajları takip etmeye başlayacaktır
    """
    
    info_label = tk.Label(
        scrollable_frame,
        text=description_text,
        font=("Arial", 10),
        justify=tk.LEFT,
        wraplength=550,
        bg="#e8f4fa",
        padx=10,
        pady=10
    )
    info_label.pack(fill=tk.X, padx=20, pady=10)
    
    # Giriş alanları için frame
    input_frame = tk.Frame(scrollable_frame)
    input_frame.pack(pady=10)
    
    tk.Label(
        input_frame,
        text="LinkedIn E-posta:",
        font=("Arial", 10, "bold")
    ).pack(pady=5)
    
    email_entry = tk.Entry(input_frame, width=40)
    email_entry.pack(pady=5)
    
    tk.Label(
        input_frame,
        text="LinkedIn Şifre:",
        font=("Arial", 10, "bold")
    ).pack(pady=5)
    
    password_entry = tk.Entry(input_frame, width=40, show="*")
    password_entry.pack(pady=5)
    
    # Başlat butonu
    start_button = tk.Button(
        input_frame,
        text="Başlat",
        font=("Arial", 12, "bold"),
        bg="#00a650",
        fg="white",
        width=20,
        height=2,
        command=lambda: start_in_thread(
            email_entry.get(),
            password_entry.get(),
            status_label,
            qr_label
        )
    )
    start_button.pack(pady=20)
    
    # Durum bildirimi için frame
    status_frame = tk.Frame(scrollable_frame, bg="#f5f5f5", width=600)
    status_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(
        status_frame,
        text="Durum:",
        font=("Arial", 10, "bold"),
        bg="#f5f5f5"
    ).pack(pady=5)
    
    status_label = tk.Label(
        status_frame,
        text="Bekleniyor...",
        font=("Arial", 10),
        bg="#f5f5f5"
    )
    status_label.pack(pady=5)
    
    # QR kod alanı
    qr_frame = tk.Frame(scrollable_frame)
    qr_frame.pack(pady=10)
    
    tk.Label(
        qr_frame,
        text="WhatsApp Web QR Kodu",
        font=("Arial", 10, "bold")
    ).pack(pady=5)
    
    qr_label = tk.Label(qr_frame)
    qr_label.pack(pady=10)
    
    # Alt bilgi
    footer_frame = tk.Frame(scrollable_frame, bg="#f0f0f0", width=600, height=40)
    footer_frame.pack(fill=tk.X, pady=10)
    footer_frame.pack_propagate(False)
    
    footer_label = tk.Label(
        footer_frame,
        text="© 2024 Tüm hakları saklıdır.",
        font=("Arial", 8),
        bg="#f0f0f0"
    )
    footer_label.pack(pady=10)
    
    # Scrollbar ve canvas yerleşimi
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Mouse wheel ile scroll desteği
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    main_container.pack(expand=True, fill="both")  # Üstteki boşluğu kaldırdık
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
