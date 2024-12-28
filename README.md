# WhatsApp ve LinkedIn Entegrasyonu

Bu proje, WhatsApp üzerinden gelen LinkedIn bağlantılarını otomatik olarak işlemek ve bağlantı istekleri göndermek için geliştirilmiş bir Python uygulamasıdır. Uygulama, bir GUI (Grafiksel Kullanıcı Arayüzü) üzerinden çalışır ve Selenium kütüphanesi kullanılarak web otomasyon işlemlerini gerçekleştirir.

## Özellikler

- WhatsApp Web üzerinden gelen LinkedIn profili bağlantılarını tarama.
- LinkedIn bağlantı isteklerini otomatik olarak gönderme.
- Kullanıcı dostu bir GUI ile kolay kullanım.

## Kullanım Talimatları

### Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki yazılımların sisteminizde kurulu olması gerekir:

- Python 3.8 veya üstü
- Google Chrome tarayıcısı
- ChromeDriver (Google Chrome sürümünüzle uyumlu olan)
- Gerekli Python kütüphaneleri:
  ```bash
  pip install -r requirements.txt
  ```

### Adımlar

1. **LinkedIn Hesap Bilgilerini Girin**: Uygulama, LinkedIn hesabınıza giriş yapmak için e-posta adresinizi ve şifrenizi gerektirir.
2. **Uygulamayı Başlatın**: Başlat butonuna tıklayarak uygulamayı çalıştırın.
3. **WhatsApp Web QR Kodunu Okutun**: Görüntülenen QR kodunu taratarak WhatsApp Web'e bağlanın.
4. **Mesajları Dinleyin**: Uygulama, seçili sohbeti dinleyerek LinkedIn bağlantılarını tespit eder ve işlem yapar.

### Önemli Not

Bu uygulama, LinkedIn oturum açtıktan sonra karşılaşılan doğrulama adımlarını (örneğin, CAPTCHA veya ikinci faktör doğrulama) otomatik olarak geçememektedir. Eğer uygulama hata veriyorsa:

- `start_process()` fonksiyonundaki **headless modunu kapatın**.
- Doğrulamayı manuel olarak çözün.
- Bu adımlardan sonra uygulama düzgün bir şekilde çalışmaya devam edecektir.

Headless modunu kapatmak için aşağıdaki adımları izleyin:

```python
# Headless mod için seçenekler oluştur (aktif olan kısmı yoruma alın veya kaldırın)
"""
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
"""
```

## Nasıl Çalışır?

1. Uygulama, WhatsApp Web'den QR kodunu alır ve GUI'de görüntüler.
2. LinkedIn'e giriş yapar ve gelen LinkedIn bağlantılarını işler.
3. Tespit edilen bağlantılara otomatik olarak bağlantı isteği gönderir.

## GUI Kullanımı

Uygulama, kullanıcı dostu bir arayüze sahiptir ve tüm işlemleri kolayca gerçekleştirmenizi sağlar:

- LinkedIn giriş bilgilerini girin.
- QR kodu taratın.
- Durum bildirimlerini ve ilerlemeyi GUI üzerinden takip edin.

## Sorun Giderme

- **Doğrulama Adımları:** LinkedIn girişinde doğrulama adımlarıyla karşılaşırsanız, doğrulamayı manuel olarak tamamlayın.
- **Bağlantı Gönderilemedi Hatası:** Belirli profillere daha önce bağlantı isteği gönderilmiş olabilir. Uygulama bu durumlarda ilgili profil hakkında bilgi verecektir.

## Katkıda Bulunma

Projeye katkıda bulunmak isterseniz lütfen bir pull request gönderin veya [geliştirici ile iletişime geçin](mailto\:tamerkanak75@gmail.com).

## Lisans

© 2024 Tüm hakları saklıdır. Bu yazılımın izinsiz kopyalanması veya dağıtılması yasaktır.

