# Kârnex AI

## Yerel Çalışan Yapay Zekâ Destekli Muhasebe Copilot'u (MSSQL Tabanlı)

---

## 1. Proje Özeti

**Kârnex AI**, mevcut muhasebe ve ERP yazılımlarının yerine geçmeyi amaçlayan bağımsız bir muhasebe programı değildir.

Projenin amacı; Mikro, Logo, ETA, Zirve ve benzeri MSSQL tabanlı muhasebe/ERP sistemlerinin yanında veya doğrudan veritabanı seviyesinde çalışabilen, kullanıcının finansal verilerini ve şirket dokümanlarını anlayarak **analiz, arama, anomali tespiti ve karar desteği sağlayan yerel bir yapay zekâ Copilot'u** geliştirmektir.

Uygulamanın temel çalışma modeli:

```text
MSSQL Veritabanı (ERP / Yerel Finansal Veri)
             │
             ▼
        Kârnex AI
             │
      ┌──────┼──────┐
      ▼      ▼      ▼
     RAG     ML    Analiz
      │      │      │
      └──────┼──────┘
             ▼
       AI Copilot
             │
             ▼
     Kullanıcıya Karar
       Desteği / Yorum
Kârnex AI'ın amacı, muhasebe çalışanının veya işletme yöneticisinin MSSQL veritabanı üzerindeki finansal verileri ve şirket dokümanlarını doğal dil kullanarak sorgulayabileceği ve yorumlayabileceği bir yapay zekâ katmanı oluşturmaktır.2. Projenin Temel AmacıProjenin ilk amacı ticari bir ERP sistemi geliştirmek değildir.Öncelikli amaç:MSSQL veritabanı bağlantısı (pyodbc / SQLAlchemy) ve SQL sorgu üretimi (Text-to-SQL) konularını öğrenmekRAG sistemlerinin çalışma mantığını öğrenmekVektör veritabanlarını ve embedding mantığını öğrenmekDoküman parçalama ve retrieval süreçlerini öğrenmekLLM'lerin harici araçlar ve veritabanları ile nasıl çalıştığını öğrenmekMakine öğrenmesi algoritmalarını MSSQL verileri üzerinde kullanmakFinansal veriler üzerinde anomaly detection uygulamakML sonuçlarını LLM ile yorumlatmakTüm bu sistemleri MSSQL tabanlı yerel bir masaüstü uygulamasında birleştirmek3. Temel VizyonKârnex AI'ın hedeflenen kullanım şekli:PlaintextKullanıcı:
"Geçen ay neden kârımız düştü?"

             ↓

Kârnex AI

             ↓

MSSQL Finansal Veriler (SQL Query)
    +
ML Analizi
    +
Şirket Dokümanları (RAG)
    +
LLM

             ↓

"Geçen aya göre satışlar %8 arttı,
ancak X ürün grubunun maliyet oranı
%14 yükseldi.

Ayrıca tedarikçi sözleşmesindeki
fiyatlandırma şartlarına göre
belirli ürünlerdeki maliyet artışı
beklenen seviyenin üzerinde."

             ↓

Kullanıcıya Açıklanabilir Sonuç
4. Masaüstü Copilot ve MSSQL MimarisiSistem yerel masaüstü uygulaması olarak çalışacak ve yerel/sunucu MSSQL veritabanına bağlanacaktır.Hedef mimari:PlaintextWindows (Kârnex AI.exe)
   │
   ├── Database Layer (pyodbc / MSSQL)
   ├── RAG Engine (Vector DB / Docs)
   ├── ML Engine (Scikit-learn / Anomaly Detection)
   ├── Analysis Engine
   ├── LLM Interface
   └── Copilot UI (PySide6)
İlk aşamada:Sistemin merkezinde örnek muhasebe şemasına sahip bir MSSQL Veritabanı bulunacaktır.FastAPI veya uzak API sunucuları ilk aşamada zorunlu değildir.Doğrudan SQL bağlantısı üzerinden veriler çekilecek ve ML/LLM katmanlarına aktarılacaktır.5. Kârnex AI'ın Temel Özellikleri5.1 AI Chat / Copilot & MSSQL SorgulamaKullanıcı doğal dil ile Kârnex AI'a soru sorabilecektir. Sistem gerektiğinde MSSQL üzerinden SQL sorguları çalıştıracak veya RAG/ML modüllerini tetikleyecektir.Örnek sorular:Plaintext"Bu ay en fazla gider hangi kategoride?" (MSSQL SQL sorgusu)

"Geçen aya göre satışlar nasıl değişti?" (MSSQL Trend Analizi)

"Bu faturada anormal bir durum var mı?" (ML Anomaly Detection)

"Şirketin satın alma prosedüründe bu kural var mı?" (RAG Doküman Arama)
6. Veritabanı ve RAG YapısıSistem iki temel veri kaynağından beslenecektir:A. MSSQL Veri Katmanı (Yapılandırılmış Veri)Fatura tabloları (Invoices)Cari hesaplar (Customers / Suppliers)Gelir/Gider hareketleri (Transactions)Stok ve Satış verileri (Inventory / Sales)B. RAG Katmanı (Yapılandırılmamış Veri)Sözleşmeler, Prosedürler, Bütçe Kuralları (PDF, DOCX, TXT vb.)Plaintext[Kullanıcı Sorusu]
       │
       ├── Yapılandırılmış Veri İhtiyacı ──> MSSQL (SQL Query) ──┐
       │                                                         ├──> [LLM Sentezi] ──> [Cevap]
       └── Doküman / Kural İhtiyacı ───────> RAG (Vector DB) ────┘
7. Makine Öğrenmesi ve MSSQL EntegrasyonuML motoru verilerini doğrudan MSSQL veritabanından çekerek işleyecektir.PlaintextMSSQL Veritabanı ──> SQL Query / Pandas DataFrame ──> Feature Engineering ──> ML Model (Isolation Forest / Z-Score) ──> Anomali Skoru ──> LLM Açıklaması
8. Teknoloji YığınıAlanTeknolojiProgramlamaPythonDesktop UIPySide6 / PyQt6VeritabanıMSSQL (pyodbc / SQLAlchemy)LLMOpenAI API veya yerel LLMEmbeddingEmbedding ModelVector DBChromaDB / FAISSMLScikit-learn / Pandas / NumPyPDF / DokümanPyMuPDFPaketlemePyInstallerVersiyon KontrolGit