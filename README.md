# 🌐 Sosyal Ağ Analizi Uygulaması

**Kocaeli Üniversitesi**  
**Teknoloji Fakültesi - Bilişim Sistemleri Mühendisliği**  
**Yazılım Geliştirme Laboratuvarı-I**  
**Proje-2**

---

## 👥 Ekip Bilgileri

| Öğrenci No | Ad Soyad |
|------------|----------|
| 231307077 | Duha Yusuf Bindere |
| 231307094 | Ahmet Öz |

**Tarih:** 1 Ocak 2026

---

## 📑 İçindekiler

1. [Giriş](#1-giriş)
2. [Problem Tanımı ve Amaç](#2-problem-tanımı-ve-amaç)
3. [Kullanılan Teknolojiler](#3-kullanılan-teknolojiler)
4. [Sistem Mimarisi ve Sınıf Yapısı](#4-sistem-mimarisi-ve-sınıf-yapısı)
5. [Algoritmalar](#5-algoritmalar)
6. [Dinamik Ağırlık Hesaplama](#6-dinamik-ağırlık-hesaplama)
7. [Kullanıcı Arayüzü](#7-kullanıcı-arayüzü)
8. [Test Sonuçları ve Performans Analizi](#8-test-sonuçları-ve-performans-analizi)
9. [Kurulum ve Çalıştırma](#9-kurulum-ve-çalıştırma)
10. [Sonuç ve Tartışma](#10-sonuç-ve-tartışma)
11. [Kaynakça](#11-kaynakça)

---

## 1. Giriş

Sosyal ağlar, günümüzde milyarlarca insanın iletişim kurduğu, bilgi paylaştığı ve topluluklar oluşturduğu dijital platformlardır. Bu ağların analizi; kullanıcı davranışlarını anlamak, toplulukları tespit etmek, etkili bireyleri belirlemek ve bilgi yayılımını modellemek açısından kritik öneme sahiptir.

Bu proje kapsamında, kullanıcılar arasındaki ilişkileri **graf veri yapısı** ile modelleyen, çeşitli **graf algoritmaları** uygulayarak sosyal ağ üzerindeki bağlantıları analiz eden interaktif bir masaüstü uygulaması geliştirilmiştir.

### Projenin Kapsamı

- Graf tabanlı sosyal ağ modelleme
- Dinamik düğüm ve kenar yönetimi
- Çoklu algoritma desteği (BFS, DFS, Dijkstra, A*, Welsh-Powell vb.)
- Görsel analiz ve renklendirme
- Veri içe/dışa aktarımı (JSON)

---

## 2. Problem Tanımı ve Amaç

### 2.1 Problem Tanımı

Sosyal ağlarda kullanıcılar arasındaki ilişkilerin analiz edilmesi, aşağıdaki soruların cevaplanmasını gerektirir:

1. **Erişilebilirlik:** Bir kullanıcıdan hangi kullanıcılara ulaşılabilir?
2. **En Kısa Yol:** İki kullanıcı arasındaki en kısa bağlantı nedir?
3. **Topluluk Tespiti:** Ağda birbirinden bağımsız kaç topluluk var?
4. **Etki Analizi:** En etkili (merkezi) kullanıcılar kimler?
5. **Renklendirme:** Komşu kullanıcıları minimum renk sayısıyla nasıl ayırt edebiliriz?

### 2.2 Amaç

Bu proje ile aşağıdaki hedeflere ulaşılması amaçlanmaktadır:

- Graf veri yapılarının etkin kullanımı
- Temel graf algoritmalarının implementasyonu
- Nesne yönelimli programlama prensiplerinin uygulanması
- Kullanıcı dostu görsel arayüz tasarımı
- Performans analizi ve optimizasyon

---

## 3. Kullanılan Teknolojiler

| Teknoloji | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| Python | 3.10+ | Ana programlama dili |
| PyQt5 | 5.15+ | Grafiksel kullanıcı arayüzü |
| JSON | - | Veri saklama formatı |

---

## 4. Sistem Mimarisi ve Sınıf Yapısı

### 4.1 Proje Dosya Yapısı

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
│   └── welsh_powell.py     # Graf renklendirme
├── data/                   # Örnek veri dosyaları
│   ├── graf_20_dugum.json
│   ├── graf_100_dugum.json
│   └── graf_100_bilesen.json
└── README.md
```

### 4.2 Sınıf Diyagramı

```mermaid
classDiagram
    class Node {
        -int node_id
        -float aktiflik
        -int etkilesim
        -int baglanti_sayisi
        -str label
        +get_id() int
        +__str__() str
        +__eq__(other) bool
        +__hash__() int
    }
    
    class Edge {
        -int source_id
        -int target_id
        -float weight
        +get_nodes() tuple
        +get_weight() float
        +set_weight(weight)
        +contains_node(node_id) bool
        +get_other_node(node_id) int
    }
    
    class Graph {
        -dict nodes
        -dict edges
        -dict adjacency
        +add_node(node_id, aktiflik, etkilesim, baglanti_sayisi, label) bool
        +remove_node(node_id) bool
        +get_node(node_id) Node
        +get_all_nodes() list
        +add_edge(node1_id, node2_id) bool
        +remove_edge(node1_id, node2_id) bool
        +get_neighbors(node_id) list
        +has_edge(node1_id, node2_id) bool
        +get_edge(node1_id, node2_id) Edge
        +update_all_weights()
    }
    
    class GraphCanvas {
        -Graph graph
        -QGraphicsScene scene
        -dict node_items
        -dict edge_items
        +draw_graph()
        +update_edges()
        +highlight_path(path)
        +apply_coloring(coloring)
        +reset_colors()
    }
    
    class ControlPanel {
        -MainWindow parent_window
        +add_node()
        +remove_node()
        +add_edge()
        +remove_edge()
        +run_bfs()
        +run_dfs()
        +run_dijkstra()
        +run_astar()
        +run_components()
        +run_centrality()
        +run_coloring()
    }
    
    class MainWindow {
        -Graph graph
        -GraphCanvas canvas
        -ControlPanel control_panel
        +load_json()
        +save_json()
    }
    
    Graph "1" *-- "many" Node : contains
    Graph "1" *-- "many" Edge : contains
    MainWindow "1" *-- "1" Graph : has
    MainWindow "1" *-- "1" GraphCanvas : has
    MainWindow "1" *-- "1" ControlPanel : has
    Edge "1" -- "2" Node : connects
```

### 4.3 Modül İlişkileri

```mermaid
flowchart TB
    subgraph UI["Kullanıcı Arayüzü"]
        main[main.py]
        gui[gui.py]
    end
    
    subgraph Models["Veri Modelleri"]
        m_node[node.py]
        m_edge[edge.py]
        m_graph[graph.py]
    end
    
    subgraph Algorithms["Algoritmalar"]
        bfs[bfs.py]
        dfs[dfs.py]
        dijkstra[dijkstra.py]
        astar[astar.py]
        components[components.py]
        centrality[centrality.py]
        welsh[welsh_powell.py]
    end
    
    subgraph Data["Veri İşleme"]
        data_io[data_io.py]
        weight[weight_calc.py]
    end
    
    main --> gui
    gui --> m_graph
    m_graph --> m_node
    m_graph --> m_edge
    m_graph --> weight
    gui --> bfs
    gui --> dfs
    gui --> dijkstra
    gui --> astar
    gui --> bagli_bilesenler
    gui --> merkezlilik
    gui --> welsh
    gui --> data_io
```

---

## 5. Algoritmalar

### 5.1 BFS (Breadth-First Search) - Genişlik Öncelikli Arama

#### Çalışma Mantığı

BFS algoritması, başlangıç düğümünden itibaren grafı katman katman (seviye seviye) dolaşır. Önce başlangıç düğümünün tüm komşuları ziyaret edilir, ardından bu komşuların komşuları ziyaret edilir ve bu şekilde devam eder.

#### Akış Diyagramı

```mermaid
flowchart TD
    A[Başla] --> B[Başlangıç düğümünü kuyruğa ekle]
    B --> C[Başlangıç düğümünü ziyaret edildi olarak işaretle]
    C --> D{Kuyruk boş mu?}
    D -->|Hayır| E[Kuyruktan düğüm çıkar]
    E --> F[Düğümü ziyaret listesine ekle]
    F --> G{Ziyaret edilmemiş komşu var mı?}
    G -->|Evet| H[Komşuyu kuyruğa ekle]
    H --> I[Komşuyu ziyaret edildi olarak işaretle]
    I --> G
    G -->|Hayır| D
    D -->|Evet| J[Ziyaret listesini döndür]
    J --> K[Bitir]
```

#### Pseudo Kod

```
BFS(Graf G, Başlangıç s):
    kuyruk ← boş kuyruk
    ziyaret_edildi ← boş küme
    
    kuyruk.ekle(s)
    ziyaret_edildi.ekle(s)
    
    while kuyruk boş değil:
        u ← kuyruk.çıkar()
        for her komşu v ∈ G.komşular(u):
            if v ∉ ziyaret_edildi:
                ziyaret_edildi.ekle(v)
                kuyruk.ekle(v)
    
    return ziyaret_edildi
```

#### Karmaşıklık Analizi

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Zaman Karmaşıklığı** | O(V + E) | V: düğüm sayısı, E: kenar sayısı |
| **Alan Karmaşıklığı** | O(V) | Kuyruk ve ziyaret listesi için |

#### Literatür

BFS algoritması ilk olarak 1959 yılında Edward F. Moore tarafından labirent çözümü için geliştirilmiştir. Daha sonra 1961'de C.Y. Lee tarafından kablo yönlendirme problemlerine uygulanmıştır [1].

---

### 5.2 DFS (Depth-First Search) - Derinlik Öncelikli Arama

#### Çalışma Mantığı

DFS algoritması, bir dalı sonuna kadar takip eder ve çıkmaza ulaştığında geri dönerek başka dalları keşfeder. Özyinelemeli veya yığın kullanarak iteratif olarak uygulanabilir.

#### Akış Diyagramı

```mermaid
flowchart TD
    A[Başla] --> B[Başlangıç düğümünü yığına ekle]
    B --> C{Yığın boş mu?}
    C -->|Hayır| D[Yığından düğüm çıkar]
    D --> E{Düğüm ziyaret edildi mi?}
    E -->|Evet| C
    E -->|Hayır| F[Düğümü ziyaret edildi olarak işaretle]
    F --> G[Düğümü ziyaret listesine ekle]
    G --> H[Tüm komşuları yığına ekle]
    H --> C
    C -->|Evet| I[Ziyaret listesini döndür]
    I --> J[Bitir]
```

#### Pseudo Kod

```
DFS(Graf G, Başlangıç s):
    yığın ← boş yığın
    ziyaret_edildi ← boş küme
    
    yığın.ekle(s)
    
    while yığın boş değil:
        u ← yığın.çıkar()
        if u ∉ ziyaret_edildi:
            ziyaret_edildi.ekle(u)
            for her komşu v ∈ G.komşular(u):
                yığın.ekle(v)
    
    return ziyaret_edildi
```

#### Karmaşıklık Analizi

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Zaman Karmaşıklığı** | O(V + E) | V: düğüm sayısı, E: kenar sayısı |
| **Alan Karmaşıklığı** | O(V) | Yığın derinliği en fazla V olabilir |

#### Literatür

DFS algoritması 19. yüzyılda labirent çözümü için Trémaux tarafından incelenmiştir. Modern formülasyonu 1972'de Hopcroft ve Tarjan tarafından yapılmıştır [2].

---

### 5.3 Dijkstra Algoritması

#### Çalışma Mantığı

Dijkstra algoritması, ağırlıklı bir grafta tek bir kaynak düğümünden diğer tüm düğümlere olan en kısa yolları bulur. Algoritma, her adımda en küçük mesafeye sahip düğümü seçer ve komşularının mesafelerini günceller.

#### Akış Diyagramı

```mermaid
flowchart TD
    A[Başla] --> B[Tüm mesafeleri ∞ olarak ayarla]
    B --> C[Başlangıç düğümünün mesafesini 0 yap]
    C --> D[Başlangıç düğümünü öncelik kuyruğuna ekle]
    D --> E{Öncelik kuyruğu boş mu?}
    E -->|Hayır| F[En küçük mesafeli düğümü çıkar]
    F --> G{Hedef düğüme ulaşıldı mı?}
    G -->|Evet| L[Yolu oluştur ve döndür]
    G -->|Hayır| H{Ziyaret edildi mi?}
    H -->|Evet| E
    H -->|Hayır| I[Düğümü ziyaret edildi olarak işaretle]
    I --> J[Her komşu için mesafeyi güncelle]
    J --> K[Güncellenenleri kuyruğa ekle]
    K --> E
    E -->|Evet| M[Yol bulunamadı]
    L --> N[Bitir]
    M --> N
```

#### Pseudo Kod

```
Dijkstra(Graf G, Başlangıç s, Hedef t):
    mesafe[v] ← ∞ for all v ∈ V
    mesafe[s] ← 0
    önceki[v] ← tanımsız for all v ∈ V
    öncelik_kuyruğu ← {(0, s)}
    
    while öncelik_kuyruğu boş değil:
        (d, u) ← öncelik_kuyruğu.en_küçüğü_çıkar()
        
        if u = t:
            return yolu_oluştur(önceki, t)
        
        for her komşu v ∈ G.komşular(u):
            yeni_mesafe ← mesafe[u] + ağırlık(u, v)
            if yeni_mesafe < mesafe[v]:
                mesafe[v] ← yeni_mesafe
                önceki[v] ← u
                öncelik_kuyruğu.ekle((yeni_mesafe, v))
    
    return yol_yok
```

#### Karmaşıklık Analizi

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Zaman Karmaşıklığı** | O((V + E) log V) | Min-heap kullanıldığında |
| **Alan Karmaşıklığı** | O(V) | Mesafe ve önceki dizileri için |

#### Literatür

Dijkstra algoritması 1956 yılında Hollandalı bilgisayar bilimcisi Edsger W. Dijkstra tarafından geliştirilmiş ve 1959'da yayınlanmıştır. En kısa yol problemleri için temel algoritma olarak kabul edilir [3].

---

### 5.4 A* (A-Star) Algoritması

#### Çalışma Mantığı

A* algoritması, Dijkstra algoritmasının sezgisel (heuristic) bir fonksiyonla genişletilmiş halidir. Her düğüm için `f(n) = g(n) + h(n)` değeri hesaplanır:
- `g(n)`: Başlangıçtan n'e olan gerçek maliyet
- `h(n)`: n'den hedefe tahmini maliyet (sezgisel)

Bu projede sezgisel fonksiyon olarak düğüm özelliklerinin Öklid mesafesi kullanılmaktadır:

```
h(n) = √[(aktiflik_n - aktiflik_hedef)² + (etkileşim_n - etkileşim_hedef)² + (bağlantı_n - bağlantı_hedef)²]
```

#### Akış Diyagramı

```mermaid
flowchart TD
    A[Başla] --> B[g ve f değerlerini ∞ olarak ayarla]
    B --> C["g(başlangıç) = 0, f(başlangıç) = h(başlangıç)"]
    C --> D[Başlangıç düğümünü açık listeye ekle]
    D --> E{Açık liste boş mu?}
    E -->|Hayır| F[En düşük f değerli düğümü seç]
    F --> G{Hedef düğüme ulaşıldı mı?}
    G -->|Evet| L[Yolu oluştur ve döndür]
    G -->|Hayır| H[Düğümü kapalı listeye ekle]
    H --> I[Her komşu için]
    I --> J["tentative_g = g(mevcut) + maliyet"]
    J --> K{"tentative_g < g(komşu)?"}
    K -->|Evet| M[Komşunun g ve f değerlerini güncelle]
    M --> N[Komşuyu açık listeye ekle]
    N --> I
    K -->|Hayır| I
    I --> E
    E -->|Evet| O[Yol bulunamadı]
    L --> P[Bitir]
    O --> P
```

#### Karmaşıklık Analizi

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Zaman Karmaşıklığı** | O(E) | En iyi durumda (iyi sezgisel ile) |
| **Zaman Karmaşıklığı** | O(b^d) | En kötü durumda (b: dallanma faktörü, d: derinlik) |
| **Alan Karmaşıklığı** | O(V) | Açık ve kapalı listeler için |

#### Literatür

A* algoritması 1968 yılında Peter Hart, Nils Nilsson ve Bertram Raphael tarafından Stanford Araştırma Enstitüsü'nde geliştirilmiştir. Kabul edilebilir (admissible) bir sezgisel fonksiyon kullanıldığında optimal çözümü garanti eder [4].

---

### 5.5 Bağlı Bileşenler (Connected Components)

#### Çalışma Mantığı

Bağlı bileşen analizi, grafta birbirine bağlı düğüm gruplarını tespit eder. Her bileşen, kendi içinde tamamen bağlı ancak diğer bileşenlerden izole bir alt graftır.

#### Akış Diyagramı

```mermaid
flowchart TD
    A[Başla] --> B[Boş bileşen listesi oluştur]
    B --> C[Tüm düğümleri işlenmemiş olarak işaretle]
    C --> D{İşlenmemiş düğüm var mı?}
    D -->|Evet| E[İşlenmemiş bir düğüm seç]
    E --> F[DFS/BFS ile tüm erişilebilir düğümleri bul]
    F --> G[Bu düğümleri yeni bileşen olarak kaydet]
    G --> H[Bu düğümleri işlenmiş olarak işaretle]
    H --> D
    D -->|Hayır| I[Bileşen listesini döndür]
    I --> J[Bitir]
```

#### Karmaşıklık Analizi

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Zaman Karmaşıklığı** | O(V + E) | Her düğüm ve kenar bir kez ziyaret edilir |
| **Alan Karmaşıklığı** | O(V) | Ziyaret listesi ve bileşen bilgisi için |

---

### 5.6 Derece Merkeziliği (Degree Centrality)

#### Çalışma Mantığı

Derece merkeziliği, bir düğümün önemini komşu sayısına göre ölçer. Yüksek derece merkeziliğine sahip düğümler, ağda daha etkili kabul edilir.

**Formül:**
```
Merkezilik(v) = derece(v) / (n - 1)
```

Burada `n` toplam düğüm sayısıdır.

#### Akış Diyagramı

```mermaid
flowchart TD
    A[Başla] --> B[Her düğüm için derece hesapla]
    B --> C["Merkezilik = derece / (n-1)"]
    C --> D[Düğümleri merkeziliğe göre sırala]
    D --> E[En yüksek 5 düğümü seç]
    E --> F[Sonuçları döndür]
    F --> G[Bitir]
```

#### Karmaşıklık Analizi

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Zaman Karmaşıklığı** | O(V + E) | Derece hesaplama |
| **Sıralama** | O(V log V) | Düğümlerin sıralanması |
| **Alan Karmaşıklığı** | O(V) | Merkezilik değerleri için |

---

### 5.7 Welsh-Powell Graf Renklendirme

#### Çalışma Mantığı

Welsh-Powell algoritması, grafı minimum renk sayısıyla boyamak için kullanılan açgözlü (greedy) bir algoritmadır. Komşu düğümlerin farklı renklere sahip olması garanti edilir.

**Algoritma Adımları:**
1. Düğümleri derecelerine göre azalan sırada sırala
2. Sırayla her düğüme, komşularında kullanılmayan en küçük rengi ata

#### Akış Diyagramı

```mermaid
flowchart TD
    A[Başla] --> B[Düğümleri dereceye göre azalan sırala]
    B --> C[İlk rengi seç]
    C --> D{İşlenmemiş düğüm var mı?}
    D -->|Evet| E[Sıradaki düğümü al]
    E --> F[Komşuların renklerini kontrol et]
    F --> G{Mevcut renk kullanılabilir mi?}
    G -->|Evet| H[Bu rengi ata]
    G -->|Hayır| I[Sonraki rengi dene]
    I --> G
    H --> D
    D -->|Hayır| J[Kullanılan renk sayısını hesapla]
    J --> K[Renklendirmeyi döndür]
    K --> L[Bitir]
```

#### Karmaşıklık Analizi

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Zaman Karmaşıklığı** | O(V² + E) | Sıralama ve renklendirme |
| **Alan Karmaşıklığı** | O(V) | Renk atamaları için |

#### Literatür

Welsh-Powell algoritması 1967 yılında D.J.A. Welsh ve M.B. Powell tarafından yayınlanmıştır. Açgözlü yaklaşım optimal sonucu garanti etmez ancak pratikte iyi sonuçlar verir [5].

---

## 6. Dinamik Ağırlık Hesaplama

### 6.1 Ağırlık Formülü

İki düğüm arasındaki kenar ağırlığı, düğümlerin özelliklerine göre dinamik olarak hesaplanır:

```
Ağırlık(i,j) = 1 / (1 + √[(Aktiflik_i - Aktiflik_j)² + (Etkileşim_i - Etkileşim_j)² + (Bağlantı_i - Bağlantı_j)²])
```

### 6.2 Formül Açıklaması

```mermaid
flowchart LR
    A[Düğüm i Özellikleri] --> C[Öklid Mesafesi Hesapla]
    B[Düğüm j Özellikleri] --> C
    C --> D["mesafe = √(Δaktiflik² + Δetkileşim² + Δbağlantı²)"]
    D --> E["ağırlık = 1 / (1 + mesafe)"]
    E --> F[Kenar Ağırlığı]
```

### 6.3 Ağırlık Özellikleri

| Durum | Mesafe | Ağırlık | Açıklama |
|-------|--------|---------|----------|
| Benzer düğümler | Küçük | Yüksek (~1) | Benzer özelliklere sahip kullanıcılar |
| Farklı düğümler | Büyük | Düşük (~0) | Farklı özelliklere sahip kullanıcılar |

### 6.4 Örnek Hesaplama

**Düğüm 1:** aktiflik=0.8, etkileşim=12, bağlantı=3  
**Düğüm 2:** aktiflik=0.6, etkileşim=8, bağlantı=2

```
mesafe = √[(0.8-0.6)² + (12-8)² + (3-2)²]
       = √[0.04 + 16 + 1]
       = √17.04
       = 4.128

ağırlık = 1 / (1 + 4.128) = 0.195
```

---

## 7. Kullanıcı Arayüzü

### 7.1 Özellikler

#### Düğüm İşlemleri
- Düğüm ekleme (ID, aktiflik, etkileşim, etiket)
- Rastgele düğüm ekleme
- Düğüm silme
- Düğüm listesi görüntüleme
- Düğüm düzenleme (çift tıklama ile)

#### Kenar İşlemleri
- Graf üzerinde seçim ile kenar ekleme
- Manuel ID girişi ile kenar ekleme
- Kenar silme

#### Algoritma Çalıştırma
- Tek buton ile algoritma tetikleme
- Parametre girişi (başlangıç/bitiş düğümü)
- Sonuçların görsel ve metin olarak gösterimi
- Çalışma süresi ölçümü

#### Görselleştirme
- Sürüklenebilir düğümler
- Kenar ağırlıklarının gösterimi
- Algoritma sonuçlarının renk kodlaması
- Yol vurgulama

### 7.2 Ekran Görüntüleri

#### Ana Ekran
![Ana Ekran](screenshots/main.png)

*Uygulamanın ana ekranı - Sol panelde kontroller, sağ panelde graf görünümü*

#### BFS Algoritması Sonucu
![BFS Sonucu](screenshots/bfs.png)

*BFS (Genişlik Öncelikli Arama) algoritması çalıştırıldıktan sonraki görünüm*

#### DFS Algoritması Sonucu
![DFS Sonucu](screenshots/dfs.png)

*DFS (Derinlik Öncelikli Arama) algoritması çalıştırıldıktan sonraki görünüm*

#### Dijkstra En Kısa Yol
![Dijkstra Sonucu](screenshots/djikstra.png)

*Dijkstra algoritması ile bulunan en kısa yol (kırmızı ile vurgulanmış)*

#### A* Algoritması Sonucu
![A* Sonucu](screenshots/A-.png)

*A* algoritması ile bulunan en kısa yol*

#### Welsh-Powell Renklendirme
![Renklendirme](screenshots/renklendirme.png)

*Welsh-Powell algoritması ile graf renklendirme sonucu - Komşu düğümler farklı renklerle boyanmış*

#### PowerShell Test Çıktısı
![PowerShell Test](screenshots/powershellTest.jpg)

*Geliştirme sürecinde algoritmaların terminal üzerinden test edilmesi*

---

## 8. Test Sonuçları ve Performans Analizi

### 8.1 Test Ortamı

| Özellik | Değer |
|---------|-------|
| İşletim Sistemi | Windows 11 |
| İşlemci | Intel Core i7 |
| RAM | 32 GB |
| Python Versiyonu | 3.14 |

### 8.2 Küçük Ölçekli Graf Testleri (20 Düğüm)

| Algoritma | Çalışma Süresi (ms) | Bellek Kullanımı | Sonuç |
|-----------|---------------------|------------------|-------|
| BFS | 0.02 | Düşük | 20 düğüm ziyaret edildi |
| DFS | 0.01 | Düşük | 20 düğüm ziyaret edildi |
| Dijkstra | 0.03 | Düşük | Yol: 5 düğüm, Maliyet: 0.4365 |
| A* | 0.02 | Düşük | Yol: 4 düğüm, Maliyet: 1.4537 |
| Bağlı Bileşenler | 0.01 | Düşük | 1 bileşen tespit edildi |
| Derece Merkeziliği | 0.01 | Düşük | Top 5 düğüm listelendi |
| Welsh-Powell | 0.02 | Düşük | 4 renk kullanıldı |

**En Merkezi 5 Düğüm (20 Düğümlü Graf):**

| Sıra | Düğüm ID | Merkezilik Değeri |
|------|----------|-------------------|
| 1 | 14 | 0.3158 |
| 2 | 2 | 0.2632 |
| 3 | 3 | 0.2632 |
| 4 | 4 | 0.2632 |
| 5 | 8 | 0.2632 |

### 8.3 Orta Ölçekli Graf Testleri (100 Düğüm)

| Algoritma | Çalışma Süresi (ms) | Bellek Kullanımı | Sonuç |
|-----------|---------------------|------------------|-------|
| BFS | 0.03 | Düşük | 100 düğüm ziyaret edildi |
| DFS | 0.05 | Düşük | 100 düğüm ziyaret edildi |
| Dijkstra | 0.11 | Düşük | Yol: 7 düğüm, Maliyet: 0.6587 |
| A* | 0.03 | Düşük | Yol: 5 düğüm, Maliyet: 1.4445 |
| Bağlı Bileşenler | 0.04 | Düşük | 1 bileşen tespit edildi |
| Derece Merkeziliği | 0.02 | Düşük | Top 5 düğüm listelendi |
| Welsh-Powell | 0.06 | Düşük | 4 renk kullanıldı |

**En Merkezi 5 Düğüm (100 Düğümlü Graf):**

| Sıra | Düğüm ID | Merkezilik Değeri |
|------|----------|-------------------|
| 1 | 16 | 0.0909 |
| 2 | 49 | 0.0909 |
| 3 | 40 | 0.0808 |
| 4 | 88 | 0.0808 |
| 5 | 95 | 0.0808 |

### 8.4 Performans Grafiği

```mermaid
xychart-beta
    title "Algoritma Performans Karşılaştırması (100 Düğüm)"
    x-axis ["BFS", "DFS", "Dijkstra", "A*", "Bağlı Bileşenler", "Merkezlilik", "Welsh-Powell"]
    y-axis "Çalışma Süresi (ms)" 0 --> 0.15
    bar [0.03, 0.05, 0.11, 0.03, 0.04, 0.02, 0.06]
```

### 8.5 Graf Bilgileri

| Graf | Düğüm Sayısı | Kenar Sayısı | Bileşen Sayısı | Kullanılan Renk |
|------|--------------|--------------|----------------|-----------------|
| Küçük Ölçekli | 20 | 40 | 1 | 4 |
| Orta Ölçekli | 100 | 227 | 1 | 4 |

### 8.6 Hata Yönetimi Test Sonuçları

| Test Senaryosu | Beklenen Davranış | Sonuç |
|----------------|-------------------|-------|
| Aynı düğüm tekrar ekleme | Hata mesajı göster | ✅ Başarılı |
| Self-loop ekleme | İşlemi engelle | ✅ Başarılı |
| Geçersiz düğüm ID | Uyarı mesajı | ✅ Başarılı |
| Boş graf üzerinde algoritma | Boş sonuç döndür | ✅ Başarılı |
| Bağlantısız düğümler arası yol | Yol bulunamadı mesajı | ✅ Başarılı |

---

## 9. Kurulum ve Çalıştırma

### 9.1 Gereksinimler

```bash
Python >= 3.7
PyQt5 >= 5.15
```

### 9.2 Kurulum

```bash
# Projeyi klonlayın
git clone https://github.com/[kullanici]/yazlab1-2.git

# Dizine gidin
cd yazlab1-2

# Bağımlılıkları yükleyin
pip install PyQt5
```

### 9.3 Çalıştırma

```bash
python main.py
```

### 9.4 Örnek Veri Yükleme

1. Uygulamayı başlatın
2. Menüden **Dosya > JSON Aç** seçin
3. `data/` klasöründen örnek bir dosya seçin:
   - `graf_20_dugum.json` - 20 düğümlü küçük graf
   - `graf_100_dugum.json` - 100 düğümlü orta ölçekli graf
   - `graf_100_bilesen.json` - 100 düğümlü 2 bileşenli graf

---

## 10. Sonuç ve Tartışma

### 10.1 Sonuç

- ✅ Tüm işlevsel isterler karşılandı
- ✅ 7 farklı graf algoritması başarıyla implemente edildi
- ✅ Dinamik ağırlık hesaplama formülü doğru çalışıyor
- ✅ İnteraktif ve kullanıcı dostu arayüz tasarlandı
- ✅ JSON formatında veri içe/dışa aktarımı sağlandı
- ✅ Nesne yönelimli tasarım prensipleri uygulandı

### 10.2 Sınırlılıklar

- Çok büyük graflar (>1000 düğüm) için performans düşebilir
- Graf görselleştirmesinde otomatik düzenleme algoritması yok
- Sadece yönsüz graflar destekleniyor
- Gerçek zamanlı güncelleme özelliği mevcut değil

### 10.3 Olası Geliştirmeler

| Geliştirme | Açıklama | Öncelik |
|------------|----------|---------|
| Yönlü graf desteği | Tek yönlü bağlantılar için | Yüksek |
| Force-directed layout | Otomatik graf düzenleme | Orta |
| Daha fazla merkezilik metrikleri | Betweenness, Closeness | Orta |
| Veritabanı entegrasyonu | SQLite desteği | Düşük |
| Graf karşılaştırma | İki graf arasında benzerlik | Düşük |

---

## 11. Kaynakça

[1] Moore, E. F. (1959). "The shortest path through a maze". Proceedings of the International Symposium on the Theory of Switching.

[2] Hopcroft, J.; Tarjan, R. (1973). "Algorithm 447: efficient algorithms for graph manipulation". Communications of the ACM. 16 (6): 372–378.

[3] Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs". Numerische Mathematik. 1: 269–271.

[4] Hart, P. E.; Nilsson, N. J.; Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths". IEEE Transactions on Systems Science and Cybernetics. 4 (2): 100–107.

[5] Welsh, D. J. A.; Powell, M. B. (1967). "An upper bound for the chromatic number of a graph and its application to timetabling problems". The Computer Journal. 10 (1): 85–86.

[6] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms (3rd ed.). MIT Press.

---