# Kârnex AI

### Yerel Çalışan Yapay Zekâ Destekli Muhasebe Copilot'u

Kârnex AI, **MSSQL tabanlı muhasebe ve ERP sistemleriyle çalışmak üzere geliştirilen**, yapay zekâ destekli bir finansal analiz ve karar destek uygulamasıdır.

Projenin temel amacı; muhasebe verilerini analiz etmek, kullanıcıların doğal dil ile finansal verilere erişmesini sağlamak ve işletmelerin finansal durumlarını daha anlaşılır şekilde değerlendirmelerine yardımcı olmaktır.

> **Finansal Zekâ, Daha İyi Kararlar.**

---

## 🚀 Projenin Amacı

Kârnex AI, mevcut muhasebe/ERP sistemlerinin yerine geçmek yerine onların verileri üzerinde çalışan bir **AI Copilot** olarak tasarlanmaktadır.

Sistem;

* Finansal verileri analiz etmeyi
* Doğal dil ile muhasebe verilerine soru sorabilmeyi
* Gelir ve giderleri incelemeyi
* Gider kategorilerini analiz etmeyi
* Kârlılık ve finansal oranları hesaplamayı
* Anormal finansal hareketleri tespit etmeyi
* Dokümanlar üzerinden bilgi almayı
* Gelecekte "What-If" senaryoları ile karar desteği sağlamayı

hedeflemektedir.

---

## 🧠 Temel Özellikler

### AI Copilot

Kullanıcı, muhasebe verileriyle ilgili sorularını doğal dil kullanarak sorabilir.

Örneğin:

```text
Toplam gelirimiz ne kadar?

Toplam giderimiz ne kadar?

En yüksek gider kategorilerimiz hangileri?

Personel giderleri toplam giderlerin yüzde kaçını oluşturuyor?

Son işlemleri göster.

Kâr marjımız nedir?
```

AI Copilot, sorunun türüne göre ilgili finansal araçları kullanarak MSSQL veritabanından gerçek verileri alır ve kullanıcıya anlaşılır bir cevap oluşturur.

---

### 🔧 Tool Calling

Kârnex AI içerisinde LLM'in doğrudan veritabanına rastgele erişmesi yerine, belirli finansal işlemler için tanımlanmış araçlar kullanılmaktadır.

Mevcut araçlardan bazıları:

* `financial_summary`
* `invoice_count`
* `top_expense_categories`
* `recent_transactions`
* `all_transactions`
* `expense_category_percentage`
* `monthly_summary`
* `expense_by_category`
* `income_by_category`
* `expense_growth`
* `profit_margin`
* `income_expense_ratio`

Bu yapı sayesinde model, finansal sorular için gerekli hesaplamaları uygulama tarafındaki kontrollü araçlar üzerinden gerçekleştirebilir.

---

## 📊 Finansal Analiz

Kârnex AI'nin mevcut analiz altyapısında;

* Toplam gelir
* Toplam gider
* Net sonuç
* Gider kategorileri
* Gelir kategorileri
* Gider yüzdeleri
* Aylık finansal özet
* Gider büyümesi
* Kâr marjı
* Gelir/gider oranı

gibi finansal metrikler hesaplanabilmektedir.

Örnek:

```text
Toplam Gelir  : 152.400 ₺
Toplam Gider  : 195.700 ₺
Net Sonuç     : -43.300 ₺
```

---

## 🚨 Anomali Tespiti

Proje içerisinde finansal işlemler üzerinde anomali tespiti gerçekleştirmek amacıyla bir makine öğrenmesi altyapısı bulunmaktadır.

Amaç;

* Olağandışı işlemleri
* Beklenmeyen giderleri
* Finansal hareketlerdeki sapmaları

tespit ederek kullanıcıya gösterebilmektir.

Anomali sistemi proje geliştikçe daha kapsamlı hale getirilecektir.

---

## 📚 RAG Sistemi

> **🚧 Geliştirme Aşamasında**

Kârnex AI içerisinde dokümanlardan bilgi alabilen bir **RAG (Retrieval-Augmented Generation)** sistemi geliştirilmektedir.

Planlanan yapı ile kullanıcı;

```text
Muhasebe politikamız nedir?

Bu gider hangi prosedüre göre işlenmeli?

Şirketin ilgili finansal dokümanında bu konu nasıl açıklanıyor?
```

gibi sorular sorabilecek ve sistem ilgili dokümanlardan bilgi getirerek cevap oluşturabilecektir.

RAG sistemi şu anda **aktif geliştirme aşamasındadır**.

---

## 🧾 Fatura Girişi

> **🚧 Geliştirme Aşamasında**

Kârnex AI içerisinde kullanıcıların uygulama üzerinden fatura ve ilgili finansal kayıtları oluşturabilmesini sağlayacak bir **fatura giriş modülü** geliştirilmektedir.

Planlanan özellikler arasında:

* Fatura oluşturma
* Müşteri / tedarikçi seçimi
* Ürün ve kategori seçimi
* Fatura kalemleri
* Gelir / gider ayrımı
* Toplam tutar hesaplama
* MSSQL veritabanına kayıt

bulunmaktadır.

Bu modül şu anda **geliştirme aşamasındadır**.

---

## 🏗️ Sistem Mimarisi

Temel mimari:

```text
                 ┌─────────────────────┐
                 │     Kârnex AI UI    │
                 │      Tkinter        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    AI Copilot       │
                 │     LLM + Tools     │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        Tool Calling       RAG           ML
             │              │              │
             ▼              ▼              ▼
          MSSQL         Documents      Anomaly
             │
             ▼
      Financial Data
```

---

## 🗄️ Veritabanı

Kârnex AI, **Microsoft SQL Server (MSSQL)** üzerinde çalışan muhasebe verileriyle çalışacak şekilde tasarlanmıştır.

Desteklenmesi hedeflenen muhasebe/ERP sistemleri:

* Micro
* Logo
* ETA
* Zirve
* MSSQL tabanlı diğer muhasebe sistemleri

Mevcut geliştirme ortamında Kârnex AI kendi MSSQL veritabanı üzerinde çalışmaktadır.

---

## 🤖 Yapay Zekâ

Kârnex AI, LLM altyapısını artık **tamamen yerel (local)** olarak çalıştırmaktadır. Model, internet bağlantısı veya harici bir API sağlayıcısı gerektirmeden **Ollama** üzerinden servis edilmektedir.

Mevcut geliştirme sürecinde kullanılan model:

```text
qwen2.5:3b-instruct-q4_K_M
```

LLM entegrasyonu, Ollama'nın sunduğu **OpenAI uyumlu API** (`http://localhost:11434/v1`) üzerinden gerçekleştirilmektedir. Bu sayede uygulama, resmi `openai` Python istemcisiyle (`OpenAI` sınıfı) doğrudan yerel modele bağlanabilmektedir.

Yerel çalışmanın sağladığı avantajlar:

* Harici bir API sağlayıcısına (ör. NVIDIA NIM) bağımlılık ortadan kalkmıştır
* API anahtarı veya internet bağlantısı gerekmeden çalışabilme
* Muhasebe verilerinin dışarıya hiç çıkmadan, tamamen yerelde işlenmesi
* API kullanım maliyeti bulunmaması

> **Not:** Proje daha önce NVIDIA API üzerinden erişilen bulut tabanlı modeller (`nvidia/nemotron-3.5-lightning-30b-a3b`) ile çalışıyordu. Güncel sürümde bu yapı kaldırılmış, yerini Ollama ile yerelde çalışan `qwen2.5:3b-instruct-q4_K_M` modeline bırakmıştır.

---

## 🛠️ Kullanılan Teknolojiler

### Backend / AI

* Python
* Microsoft SQL Server
* OpenAI-compatible API
* Ollama (yerel LLM çalıştırma)
* LLM Tool Calling
* Machine Learning
* RAG

### GUI

* Tkinter
* ttk
* Matplotlib
* Pillow

### Geliştirme

* Git
* GitHub
* Python Virtual Environment
* python-dotenv

---

## 📁 Proje Yapısı

```text
KârnexAi/
│
├── app/
│   ├── ai/
│   │   ├── database.py
│   │   ├── llm_client.py
│   │   ├── prompts.py
│   │   ├── tool_registry.py
│   │   └── tools.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── queries.py
│   │
│   ├── ml/
│   │   └── anomaly.py
│   │
│   ├── rag/
│   │
│   ├── services/
│   │
│   ├── ui/
│   │   ├── dashboard.py
│   │   └── karnex.ico
│   │
│   └── main.py
│
├── data/
├── documents/
├── tests/
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Kurulum

### 1. Repoyu klonlayın

```bash
git clone https://github.com/USERNAME/KârnexAi.git
cd KârnexAi
```

### 2. Virtual Environment oluşturun

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Gereksinimleri yükleyin

```bash
pip install -r requirements.txt
```

### 4. Ollama'yı kurun ve modeli indirin

Kârnex AI, LLM olarak **Ollama** üzerinden yerel bir modeli kullanmaktadır. Öncelikle [Ollama](https://ollama.com)'yı bilgisayarınıza kurun, ardından kullanılan modeli indirin:

```bash
ollama pull qwen2.5:3b-instruct-q4_K_M
```

Ollama servisinin varsayılan olarak `http://localhost:11434` adresinde çalıştığından emin olun.

### 5. `.env` dosyasını oluşturun

```env
DB_SERVER=YOUR_SQL_SERVER
DB_NAME=YOUR_DATABASE
```

> Ollama yerelde çalıştığı ve gerçek bir API anahtarı kontrolü yapmadığı için ayrı bir API anahtarı tanımlamanıza gerek yoktur.

### 6. Uygulamayı çalıştırın

```bash
python -m app.main
```

---

## 🔐 Güvenlik

`.env` dosyası içerisinde bulunan;

* Veritabanı kullanıcı bilgileri
* Şifreler
* Özel bağlantı bilgileri

GitHub reposuna gönderilmemelidir.

`.gitignore` içerisinde `.env` dosyasının bulunduğundan emin olun.

---

## 🗺️ Geliştirme Yol Haritası

### ✅ Tamamlanan / Çalışan

* [x] MSSQL bağlantısı
* [x] Temel finansal veritabanı yapısı
* [x] Finansal sorgular
* [x] AI Copilot altyapısı
* [x] LLM entegrasyonu (Ollama üzerinden yerel çalışma)
* [x] Tool Calling
* [x] Finansal analiz araçları
* [x] Temel anomali tespit altyapısı
* [x] Tkinter dashboard
* [x] AI Chat arayüzü

### 🚧 Geliştirme Aşamasında

* [ ] RAG sistemi
* [ ] Doküman yükleme ve indeksleme
* [ ] Fatura giriş modülü
* [ ] Fatura detaylarının MSSQL'e kaydedilmesi
* [ ] RAG + AI Copilot entegrasyonu
* [ ] Daha gelişmiş anomali tespiti
* [ ] Finansal raporlama

### 🔮 Planlanan

* [ ] What-If analizleri
* [ ] Finansal tahminleme
* [ ] Gelişmiş maliyet analizi
* [ ] Maliyet kaçağı tespiti
* [ ] Otomatik finansal rapor oluşturma
* [ ] Daha gelişmiş ERP entegrasyonları
* [ ] Daha kapsamlı karar destek sistemi

---

## 🎯 Projenin Vizyonu

Kârnex AI'nin uzun vadeli hedefi, işletmelerin mevcut muhasebe verilerini yalnızca raporlayan değil, bu verileri **anlayan, analiz eden ve kullanıcıyla doğal dil üzerinden etkileşime giren bir finansal AI Copilot** haline gelmesidir.

Sistem geliştikçe;

```text
Muhasebe Verisi
       ↓
     MSSQL
       ↓
   Kârnex AI
       ↓
 ┌─────┼─────┐
 ↓     ↓     ↓
LLM   RAG    ML
 ↓     ↓     ↓
 └─────┼─────┘
       ↓
 Finansal Analiz
       ↓
 Karar Desteği
```

yapısının oluşturulması hedeflenmektedir.

---

## 📌 Proje Durumu

**Kârnex AI aktif geliştirme aşamasındadır.**

Projenin temel MSSQL, AI Copilot, Tool Calling ve finansal analiz altyapıları geliştirilmektedir.

**RAG sistemi ve fatura giriş modülü ise şu anda geliştirme aşamasındadır ve henüz tamamlanmamıştır.**

Bu nedenle proje şu an **production-ready bir muhasebe yazılımı değil, aktif olarak geliştirilen bir AI finansal analiz ve karar destek projesidir.**

---

## 👨‍💻 Geliştirici

**Muhammet Hüseyin Salman**

Computer Engineering

---

## 📄 Lisans

Bu proje geliştirme aşamasındadır. Lisans bilgileri daha sonra eklenecektir.