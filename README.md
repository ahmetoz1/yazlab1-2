# 🌐 Sosyal Ağ Analizi Programı

Sosyal ağ yapılarını görselleştirmek, analiz etmek ve üzerinde çeşitli graf algoritmaları çalıştırmak için geliştirilmiş Python tabanlı bir masaüstü uygulamasıdır.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Veri Modelleri](#-veri-modelleri)
- [Algoritmalar](#-algoritmalar)
- [Dosya Formatları](#-dosya-formatları)
- [Ekran Görüntüleri](#-ekran-görüntüleri)

## ✨ Özellikler

### Graf İşlemleri
- **Düğüm Yönetimi**: Düğüm ekleme, silme ve düzenleme
- **Kenar Yönetimi**: Düğümler arası bağlantı ekleme ve silme
- **Otomatik Ağırlık Hesaplama**: Düğüm özelliklerine göre kenar ağırlıkları otomatik hesaplanır
- **Sürükle-Bırak**: Düğümleri fare ile taşıyarak graf düzenini özelleştirme

### Görselleştirme
- **İnteraktif Graf Görünümü**: Düğümleri ve kenarları görsel olarak gösterir
- **Renk Kodlaması**: Algoritma sonuçlarını renklerle görselleştirir
- **Ağırlık Gösterimi**: Kenar ağırlıkları graf üzerinde gösterilir

### Algoritmalar
- **BFS (Breadth-First Search)**: Genişlik öncelikli arama
- **DFS (Depth-First Search)**: Derinlik öncelikli arama
- **Dijkstra**: En kısa yol algoritması
- **A\* (A-Star)**: Sezgisel en kısa yol algoritması
- **Bağlı Bileşenler**: Graf bileşen analizi
- **Derece Merkeziliği**: Düğüm önem sıralaması
- **Welsh-Powell Renklendirme**: Graf renklendirme algoritması

### Veri Yönetimi
- **JSON İçe/Dışa Aktarma**: Graf verilerini JSON formatında kaydetme ve yükleme
- **CSV Desteği**: CSV formatında veri işleme

## 🔧 Kurulum

### Gereksinimler
- Python 3.7 veya üzeri
- PyQt5

### Bağımlılıkları Yükleme

```bash
pip install PyQt5
```

### Uygulamayı Çalıştırma

```bash
cd yazlab1-2
python main.py
```

## 🚀 Kullanım

### Temel İşlemler

#### Düğüm Ekleme
1. Sol panelde "Düğüm İşlemleri" bölümünü kullanın
2. Düğüm ID, aktiflik (0-1 arası), etkileşim ve etiket bilgilerini girin
3. "Düğüm Ekle" butonuna tıklayın

#### Kenar Ekleme
1. Graf üzerinde iki düğüme tıklayarak seçin (sarı kenarlık ile gösterilir)
2. Veya "Kenar İşlemleri" bölümünde düğüm ID'lerini manuel girin
3. "Kenar Ekle" butonuna tıklayın

#### Düğüm Bilgisi Görüntüleme
- Herhangi bir düğüme çift tıklayarak detaylarını görüntüleyin
- Açılan pencereden düğümü düzenleyebilirsiniz

### Algoritmaları Çalıştırma

1. Sol paneldeki "Algoritmalar" bölümünden istediğiniz algoritmayı seçin
2. Gerekli parametreleri girin (başlangıç/bitiş düğümü)
3. Sonuçlar hem metin olarak hem de graf üzerinde renklerle gösterilir

### Dosya İşlemleri

- **Dosya > JSON Aç**: Kayıtlı bir graf dosyasını yükler
- **Dosya > JSON Kaydet**: Mevcut grafı dosyaya kaydeder

## 📁 Proje Yapısı

```
yazlab1-2/
├── main.py                 # Ana giriş noktası
├── gui.py                  # Ana GUI bileşenleri
├── data_io.py              # Veri okuma/yazma işlemleri
├── weight_calc.py          # Kenar ağırlık hesaplama
├── models/                 # Veri modelleri
│   ├── node.py             # Düğüm (Node) sınıfı
│   ├── edge.py             # Kenar (Edge) sınıfı
│   └── graph.py            # Graf sınıfı
├── algorithms/             # Algoritmalar
│   ├── bfs.py              # Genişlik öncelikli arama
│   ├── dfs.py              # Derinlik öncelikli arama
│   ├── dijkstra.py         # Dijkstra algoritması
│   ├── astar.py            # A* algoritması
│   ├── components.py       # Bağlı bileşen analizi
│   ├── centrality.py       # Derece merkeziliği
│   ├── welsh_powell.py     # Graf renklendirme
│   └── gui.py              # Algoritma GUI (alternatif)
├── data/                   # Örnek veri dosyaları
│   ├── graf_20_dugum.json  # 20 düğümlü örnek graf
│   ├── graf_100_dugum.json # 100 düğümlü örnek graf
│   └── graf_100_bilesen.json # 100 bileşenli örnek graf
└── README.md               # Bu dosya
```

## 📊 Veri Modelleri

### Node (Düğüm)

Her düğüm bir sosyal ağ kullanıcısını temsil eder.

| Özellik | Tür | Açıklama |
|---------|-----|----------|
| `node_id` | int | Benzersiz düğüm kimliği |
| `aktiflik` | float | Kullanıcı aktiflik oranı (0-1) |
| `etkilesim` | int | Toplam etkileşim sayısı |
| `baglanti_sayisi` | int | Bağlantı (arkadaş) sayısı |
| `label` | str | Düğüm etiketi/adı |

### Edge (Kenar)

Her kenar iki kullanıcı arasındaki bağlantıyı temsil eder.

| Özellik | Tür | Açıklama |
|---------|-----|----------|
| `source_id` | int | Kaynak düğüm ID |
| `target_id` | int | Hedef düğüm ID |
| `weight` | float | Bağlantı ağırlığı (0-1) |

### Ağırlık Hesaplama

Kenar ağırlıkları, bağlı düğümlerin özelliklerine göre hesaplanır:

```
distance = √[(aktiflik₁ - aktiflik₂)² + (etkileşim₁ - etkileşim₂)² + (bağlantı₁ - bağlantı₂)²]
weight = 1 / (1 + distance)
```

Bu formül, benzer özelliklere sahip kullanıcılar arasında daha yüksek ağırlık değerleri üretir.

## 🔬 Algoritmalar

### BFS (Genişlik Öncelikli Arama)

Başlangıç düğümünden itibaren katman katman tüm erişilebilir düğümleri ziyaret eder.

**Çıktı:** Ziyaret sırası ve her düğümün seviyesi

**Görselleştirme:** Seviyeye göre gradyan renkler (kırmızıdan sarıya)

### DFS (Derinlik Öncelikli Arama)

Başlangıç düğümünden itibaren bir dal boyunca en derine giderek arama yapar.

**Çıktı:** Ziyaret sırası ve keşif zamanları

**Görselleştirme:** Keşif sırasına göre yeşil tonları

### Dijkstra Algoritması

İki düğüm arasındaki en kısa yolu bulur (ağırlıklı kenarlar).

**Çıktı:** En kısa yol ve toplam maliyet

**Görselleştirme:** Yol kırmızı renkle vurgulanır

### A* Algoritması

Sezgisel fonksiyon kullanarak en kısa yolu bulur.

**Sezgisel Fonksiyon:**
```
h(n) = √[(aktiflik_n - aktiflik_hedef)² + (etkileşim_n - etkileşim_hedef)² + (bağlantı_n - bağlantı_hedef)²]
```

**Çıktı:** En kısa yol ve toplam maliyet

**Görselleştirme:** Yol kırmızı renkle vurgulanır

### Bağlı Bileşenler

Graftaki birbirine bağlı düğüm gruplarını tespit eder.

**Çıktı:** Bileşen sayısı ve her bileşendeki düğümler

### Derece Merkeziliği

Her düğümün "önemini" komşu sayısına göre hesaplar.

**Formül:** `merkezilik = derece / (n - 1)`

**Çıktı:** En merkezi 5 düğüm ve değerleri

### Welsh-Powell Renklendirme

Grafı, komşu düğümlerin farklı renklere sahip olacağı şekilde minimum renk sayısıyla renklendirir.

**Algoritma:**
1. Düğümleri derece sırasına göre azalan şekilde sırala
2. Her düğüme, komşularında kullanılmayan en küçük rengi ata

**Çıktı:** Kullanılan renk sayısı ve renk atamaları

## 📄 Dosya Formatları

### JSON Format

```json
{
  "nodes": [
    {
      "id": 1,
      "aktiflik": 0.8,
      "etkilesim": 12,
      "baglanti_sayisi": 3,
      "label": "Kullanici 1",
      "x": 150,
      "y": 200
    }
  ],
  "edges": [
    {
      "source": 1,
      "target": 2,
      "weight": 0.75
    }
  ]
}
```

### CSV Format (İki Dosya)

**nodes.csv:**
```csv
id,aktiflik,etkilesim,baglanti_sayisi,label
1,0.8,12,3,Kullanici 1
```

**edges.csv:**
```csv
source,target,weight
1,2,0.75
```

## 🖼️ Ekran Görüntüleri

Uygulama şu ana bileşenlerden oluşur:

1. **Sol Panel (Kontrol Paneli)**
   - Düğüm işlemleri
   - Kenar işlemleri
   - Algoritma butonları
   - Sonuç görüntüleme alanı

2. **Sağ Panel (Graf Görünümü)**
   - İnteraktif graf görselleştirme
   - Sürüklenebilir düğümler
   - Ağırlıklı kenarlar

3. **Menü Çubuğu**
   - Dosya işlemleri (Aç, Kaydet, Çıkış)

## 🛠️ Geliştirme

### Yeni Algoritma Ekleme

1. `algorithms/` klasörüne yeni bir Python dosyası oluşturun
2. Graf nesnesini parametre olarak alan bir fonksiyon yazın
3. `gui.py` dosyasında ilgili butonu ve bağlantısını ekleyin

### Özelleştirme

- **Renkler**: `gui.py` içindeki renk kodlarını değiştirin
- **Düğüm Boyutu**: `NodeItem` sınıfında `radius` parametresini ayarlayın
- **Varsayılan Değerler**: `models/node.py` içindeki varsayılan parametreleri değiştirin

