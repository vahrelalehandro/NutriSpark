"""
NutriSpark Expert System
Rule-Based Expert System dengan Forward Chaining untuk Analisis Nutrisi Makanan
"""

import re
from typing import Dict, List, Optional, Tuple


class KnowledgeBase:
    """Knowledge Base untuk menyimpan data makanan dan aturan kesehatan"""
    
    def __init__(self):
        # Database Makanan
        self.food_database = {
            # Sayuran
            'tomat': {
                'type': 'sayuran',
                'nutrition': {
                    'Kalori': 18,
                    'Karbohidrat': 3.9,
                    'Protein': 0.9,
                    'Lemak': 0.2,
                    'Serat': 1.2,
                    'Vitamin C': 14,
                    'Air': 95
                },
                'unit': {'Kalori': 'kcal', 'Vitamin C': 'mg', 'Air': '%'}
            },
            'wortel': {
                'type': 'sayuran',
                'nutrition': {
                    'Kalori': 41,
                    'Karbohidrat': 9.6,
                    'Protein': 0.9,
                    'Lemak': 0.2,
                    'Serat': 2.8,
                    'Vitamin A': 835,
                    'Air': 88
                },
                'unit': {'Kalori': 'kcal', 'Vitamin A': 'mcg', 'Air': '%'}
            },
            'brokoli': {
                'type': 'sayuran',
                'nutrition': {
                    'Kalori': 34,
                    'Karbohidrat': 7,
                    'Protein': 2.8,
                    'Lemak': 0.4,
                    'Serat': 2.6,
                    'Vitamin C': 89,
                    'Kalsium': 47
                },
                'unit': {'Kalori': 'kcal', 'Vitamin C': 'mg', 'Kalsium': 'mg'}
            },
            'bayam': {
                'type': 'sayuran',
                'nutrition': {
                    'Kalori': 23,
                    'Karbohidrat': 3.6,
                    'Protein': 2.9,
                    'Lemak': 0.4,
                    'Serat': 2.2,
                    'Zat Besi': 2.7,
                    'Vitamin K': 483
                },
                'unit': {'Kalori': 'kcal', 'Zat Besi': 'mg', 'Vitamin K': 'mcg'}
            },
            
            # Buah
            'apel': {
                'type': 'buah',
                'nutrition': {
                    'Kalori': 52,
                    'Karbohidrat': 14,
                    'Protein': 0.3,
                    'Lemak': 0.2,
                    'Serat': 2.4,
                    'Vitamin C': 5,
                    'Air': 86
                },
                'unit': {'Kalori': 'kcal', 'Vitamin C': 'mg', 'Air': '%'}
            },
            'pisang': {
                'type': 'buah',
                'nutrition': {
                    'Kalori': 89,
                    'Karbohidrat': 23,
                    'Protein': 1.1,
                    'Lemak': 0.3,
                    'Serat': 2.6,
                    'Kalium': 358,
                    'Vitamin B6': 0.4
                },
                'unit': {'Kalori': 'kcal', 'Kalium': 'mg', 'Vitamin B6': 'mg'}
            },
            'jeruk': {
                'type': 'buah',
                'nutrition': {
                    'Kalori': 47,
                    'Karbohidrat': 12,
                    'Protein': 0.9,
                    'Lemak': 0.1,
                    'Serat': 2.4,
                    'Vitamin C': 53,
                    'Folat': 30
                },
                'unit': {'Kalori': 'kcal', 'Vitamin C': 'mg', 'Folat': 'mcg'}
            },
            'mangga': {
                'type': 'buah',
                'nutrition': {
                    'Kalori': 60,
                    'Karbohidrat': 15,
                    'Protein': 0.8,
                    'Lemak': 0.4,
                    'Serat': 1.6,
                    'Vitamin A': 54,
                    'Vitamin C': 36
                },
                'unit': {'Kalori': 'kcal', 'Vitamin A': 'mcg', 'Vitamin C': 'mg'}
            },
            
            # Makanan Lain
            'nasi': {
                'type': 'makanan',
                'nutrition': {
                    'Kalori': 130,
                    'Karbohidrat': 28,
                    'Protein': 2.7,
                    'Lemak': 0.3,
                    'Serat': 0.4,
                    'Zat Besi': 0.2,
                    'Vitamin B1': 0.02
                },
                'unit': {'Kalori': 'kcal', 'Zat Besi': 'mg', 'Vitamin B1': 'mg'}
            },
            'ayam': {
                'type': 'makanan',
                'nutrition': {
                    'Kalori': 165,
                    'Karbohidrat': 0,
                    'Protein': 31,
                    'Lemak': 3.6,
                    'Serat': 0,
                    'Zat Besi': 0.9,
                    'Vitamin B12': 0.3
                },
                'unit': {'Kalori': 'kcal', 'Zat Besi': 'mg', 'Vitamin B12': 'mcg'}
            },
            'telur': {
                'type': 'makanan',
                'nutrition': {
                    'Kalori': 155,
                    'Karbohidrat': 1.1,
                    'Protein': 13,
                    'Lemak': 11,
                    'Serat': 0,
                    'Vitamin D': 2,
                    'Vitamin B12': 0.9
                },
                'unit': {'Kalori': 'kcal', 'Vitamin D': 'mcg', 'Vitamin B12': 'mcg'}
            },
            'ikan': {
                'type': 'makanan',
                'nutrition': {
                    'Kalori': 206,
                    'Karbohidrat': 0,
                    'Protein': 22,
                    'Lemak': 12,
                    'Omega-3': 2.3,
                    'Vitamin D': 10,
                    'Selenium': 36
                },
                'unit': {'Kalori': 'kcal', 'Vitamin D': 'mcg', 'Selenium': 'mcg'}
            }
        }
        
        # Rules untuk Health Tips
        self.health_rules = {
            'general': [
                'Kesehatan tubuh optimal dapat dicapai melalui pola makan seimbang dan teratur.',
                'Konsumsi makanan dengan kombinasi karbohidrat, protein, lemak sehat, vitamin, dan mineral.',
                'Minum air putih secara teratur untuk menjaga keseimbangan cairan tubuh.',
                'Mengatur porsi makan dengan prinsip "setengah piring sayur dan buah".',
                'Istirahat cukup dan pengelolaan stres adalah bagian dari gaya hidup sehat.'
            ],
            'sayuran': [
                'Sayuran kaya serat yang membantu pencernaan dan kesehatan usus.',
                'Konsumsi sayuran beragam warna untuk berbagai vitamin dan mineral.',
                'Sayuran hijau mengandung antioksidan yang melindungi sel tubuh.'
            ],
            'buah': [
                'Buah-buahan adalah sumber vitamin C alami untuk sistem kekebalan tubuh.',
                'Konsumsi buah utuh lebih baik daripada jus karena lebih banyak serat.',
                'Buah segar memberikan energi alami dan menjaga hidrasi tubuh.'
            ],
            'protein_tinggi': [
                'Protein penting untuk membangun dan memperbaiki jaringan tubuh.',
                'Pilih sumber protein rendah lemak untuk kesehatan jantung.',
                'Kombinasikan protein hewani dan nabati untuk asam amino lengkap.'
            ],
            'karbohidrat_tinggi': [
                'Pilih karbohidrat kompleks untuk energi yang lebih tahan lama.',
                'Karbohidrat adalah sumber energi utama untuk aktivitas harian.',
                'Batasi karbohidrat sederhana untuk menjaga kadar gula darah stabil.'
            ],
            'serat_tinggi': [
                'Serat membantu melancarkan pencernaan dan mencegah sembelit.',
                'Konsumsi serat cukup dapat menurunkan risiko penyakit jantung.',
                'Serat membantu mengontrol berat badan dengan memberikan rasa kenyang lebih lama.'
            ],
            'hidrasi': [
                'Makanan tinggi air membantu menjaga hidrasi tubuh.',
                'Hidrasi baik mendukung fungsi organ dan metabolisme tubuh.',
                'Air membantu transportasi nutrisi ke seluruh tubuh.'
            ]
        }
    
    def get_food(self, food_name: str) -> Optional[Dict]:
        """Mendapatkan data makanan dari knowledge base"""
        return self.food_database.get(food_name.lower())
    
    def get_all_foods(self) -> List[str]:
        """Mendapatkan semua nama makanan"""
        return list(self.food_database.keys())
    
    def get_foods_by_type(self, food_type: str) -> List[str]:
        """Mendapatkan makanan berdasarkan tipe"""
        return [name for name, data in self.food_database.items() 
                if data['type'] == food_type]


class InferenceEngine:
    """Forward Chaining Inference Engine"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.working_memory = {}
        
    def analyze_food(self, food_name: str) -> Dict:
        """
        Menganalisis makanan dan menerapkan forward chaining
        untuk menghasilkan rekomendasi kesehatan
        """
        food_data = self.kb.get_food(food_name)
        
        if not food_data:
            return {
                'status': 'error',
                'message': f'Makanan "{food_name}" tidak ditemukan dalam database'
            }
        
        # Reset working memory
        self.working_memory = {
            'food_name': food_name,
            'food_type': food_data['type'],
            'nutrition': food_data['nutrition'],
            'unit': food_data.get('unit', {}),
            'facts': [],
            'recommendations': []
        }
        
        # Forward Chaining Process
        self._apply_rules()
        
        return {
            'status': 'success',
            'food_name': food_name.capitalize(),
            'type': food_data['type'],
            'nutrition': self._format_nutrition(),
            'facts': self.working_memory['facts'],
            'recommendations': self.working_memory['recommendations']
        }
    
    def _apply_rules(self):
        """Menerapkan aturan forward chaining"""
        nutrition = self.working_memory['nutrition']
        food_type = self.working_memory['food_type']
        
        # Rule 1: Analisis Kategori Makanan
        if food_type == 'sayuran':
            self.working_memory['facts'].append('Termasuk dalam kategori sayuran')
            self.working_memory['recommendations'].extend(self.kb.health_rules['sayuran'])
        elif food_type == 'buah':
            self.working_memory['facts'].append('Termasuk dalam kategori buah-buahan')
            self.working_memory['recommendations'].extend(self.kb.health_rules['buah'])
        
        # Rule 2: Analisis Kalori
        kalori = nutrition.get('Kalori', 0)
        if kalori < 50:
            self.working_memory['facts'].append('Makanan rendah kalori (< 50 kcal)')
            self.working_memory['recommendations'].append('Cocok untuk program diet rendah kalori.')
        elif kalori > 150:
            self.working_memory['facts'].append('Makanan tinggi kalori (> 150 kcal)')
            self.working_memory['recommendations'].append('Konsumsi dalam porsi yang tepat untuk mengontrol asupan kalori.')
        
        # Rule 3: Analisis Protein
        protein = nutrition.get('Protein', 0)
        if protein > 10:
            self.working_memory['facts'].append(f'Tinggi protein ({protein}g)')
            self.working_memory['recommendations'].extend(self.kb.health_rules['protein_tinggi'][:2])
        elif protein > 5:
            self.working_memory['facts'].append(f'Sumber protein sedang ({protein}g)')
        
        # Rule 4: Analisis Karbohidrat
        karbo = nutrition.get('Karbohidrat', 0)
        if karbo > 20:
            self.working_memory['facts'].append(f'Tinggi karbohidrat ({karbo}g)')
            self.working_memory['recommendations'].extend(self.kb.health_rules['karbohidrat_tinggi'][:2])
        elif karbo < 5:
            self.working_memory['facts'].append(f'Rendah karbohidrat ({karbo}g)')
            self.working_memory['recommendations'].append('Cocok untuk diet rendah karbohidrat.')
        
        # Rule 5: Analisis Serat
        serat = nutrition.get('Serat', 0)
        if serat > 2:
            self.working_memory['facts'].append(f'Tinggi serat ({serat}g)')
            self.working_memory['recommendations'].extend(self.kb.health_rules['serat_tinggi'][:2])
        
        # Rule 6: Analisis Lemak
        lemak = nutrition.get('Lemak', 0)
        if lemak < 1:
            self.working_memory['facts'].append('Sangat rendah lemak')
            self.working_memory['recommendations'].append('Pilihan baik untuk diet rendah lemak.')
        elif lemak > 10:
            self.working_memory['facts'].append(f'Tinggi lemak ({lemak}g)')
            self.working_memory['recommendations'].append('Perhatikan porsi konsumsi untuk mengontrol asupan lemak.')
        
        # Rule 7: Analisis Hidrasi
        air = nutrition.get('Air', 0)
        if air > 85:
            self.working_memory['facts'].append(f'Sangat tinggi kandungan air ({air}%)')
            self.working_memory['recommendations'].extend(self.kb.health_rules['hidrasi'][:2])
        
        # Rule 8: Analisis Vitamin C
        vit_c = nutrition.get('Vitamin C', 0)
        if vit_c > 50:
            self.working_memory['facts'].append(f'Sangat tinggi Vitamin C ({vit_c}mg)')
            self.working_memory['recommendations'].append('Vitamin C tinggi meningkatkan sistem kekebalan tubuh.')
        elif vit_c > 10:
            self.working_memory['facts'].append(f'Sumber Vitamin C yang baik ({vit_c}mg)')
        
        # Rule 9: Rekomendasi Umum
        self.working_memory['recommendations'].extend(self.kb.health_rules['general'][:2])
        
        # Batasi jumlah rekomendasi
        self.working_memory['recommendations'] = list(set(self.working_memory['recommendations']))[:6]
    
    def _format_nutrition(self) -> Dict[str, str]:
        """Format data nutrisi dengan unit yang sesuai"""
        nutrition = self.working_memory['nutrition']
        unit_map = self.working_memory['unit']
        formatted = {}
        
        default_units = {
            'Kalori': 'kcal',
            'Karbohidrat': 'g',
            'Protein': 'g',
            'Lemak': 'g',
            'Serat': 'g',
            'Air': '%'
        }
        
        for nutrient, value in nutrition.items():
            unit = unit_map.get(nutrient, default_units.get(nutrient, 'g'))
            formatted[nutrient] = f"{value} {unit}"
        
        return formatted
    
    def compare_foods(self, food1: str, food2: str) -> Dict:
        """Membandingkan dua makanan"""
        data1 = self.analyze_food(food1)
        data2 = self.analyze_food(food2)
        
        if data1['status'] == 'error' or data2['status'] == 'error':
            return {
                'status': 'error',
                'message': 'Salah satu makanan tidak ditemukan'
            }
        
        comparison = {
            'status': 'success',
            'food1': data1,
            'food2': data2,
            'comparison': self._generate_comparison(data1, data2)
        }
        
        return comparison
    
    def _generate_comparison(self, data1: Dict, data2: Dict) -> List[str]:
        """Generate perbandingan antar makanan"""
        comparisons = []
        
        n1 = self.kb.get_food(data1['food_name'].lower())['nutrition']
        n2 = self.kb.get_food(data2['food_name'].lower())['nutrition']
        
        # Bandingkan kalori
        if n1['Kalori'] > n2['Kalori']:
            diff = n1['Kalori'] - n2['Kalori']
            comparisons.append(f"{data1['food_name']} memiliki kalori {diff} kcal lebih tinggi")
        elif n2['Kalori'] > n1['Kalori']:
            diff = n2['Kalori'] - n1['Kalori']
            comparisons.append(f"{data2['food_name']} memiliki kalori {diff} kcal lebih tinggi")
        
        # Bandingkan protein
        if n1['Protein'] > n2['Protein']:
            comparisons.append(f"{data1['food_name']} lebih tinggi protein")
        elif n2['Protein'] > n1['Protein']:
            comparisons.append(f"{data2['food_name']} lebih tinggi protein")
        
        # Bandingkan serat
        if n1.get('Serat', 0) > n2.get('Serat', 0):
            comparisons.append(f"{data1['food_name']} lebih tinggi serat")
        elif n2.get('Serat', 0) > n1.get('Serat', 0):
            comparisons.append(f"{data2['food_name']} lebih tinggi serat")
        
        return comparisons
    
    def find_foods_by_nutrient(self, nutrient: str, min_value: float = 0) -> List[Tuple[str, float]]:
        """Mencari makanan berdasarkan nutrient tertentu"""
        results = []
        
        for food_name, food_data in self.kb.food_database.items():
            nutrition = food_data['nutrition']
            if nutrient in nutrition:
                value = nutrition[nutrient]
                if value >= min_value:
                    results.append((food_name, value))
        
        # Sort by value (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        return results


class ExpertSystemInterface:
    """Interface untuk berinteraksi dengan sistem pakar"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
        self.inference_engine = InferenceEngine(self.kb)
    
    def analyze(self, food_name: str):
        """Analisis makanan dengan output yang terformat"""
        result = self.inference_engine.analyze_food(food_name)
        
        if result['status'] == 'error':
            print(f"\n❌ ERROR: {result['message']}")
            print(f"Makanan yang tersedia: {', '.join(self.kb.get_all_foods())}")
            return
        
        print("\n" + "="*70)
        print(f"🍎 ANALISIS NUTRISI: {result['food_name'].upper()}")
        print("="*70)
        
        print(f"\n📂 Kategori: {result['type'].capitalize()}")
        
        print("\n📊 KANDUNGAN NUTRISI (per 100g):")
        print("-"*70)
        for nutrient, value in result['nutrition'].items():
            print(f"  • {nutrient:<20}: {value:>10}")
        
        print("\n🔍 FAKTA NUTRISI:")
        print("-"*70)
        for i, fact in enumerate(result['facts'], 1):
            print(f"  {i}. {fact}")
        
        print("\n💡 REKOMENDASI KESEHATAN:")
        print("-"*70)
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print("\n" + "="*70)
    
    def compare(self, food1: str, food2: str):
        """Bandingkan dua makanan"""
        result = self.inference_engine.compare_foods(food1, food2)
        
        if result['status'] == 'error':
            print(f"\n❌ ERROR: {result['message']}")
            return
        
        print("\n" + "="*70)
        print(f"⚖️  PERBANDINGAN: {food1.upper()} vs {food2.upper()}")
        print("="*70)
        
        print(f"\n📊 {result['food1']['food_name']}:")
        for nutrient, value in list(result['food1']['nutrition'].items())[:5]:
            print(f"  • {nutrient}: {value}")
        
        print(f"\n📊 {result['food2']['food_name']}:")
        for nutrient, value in list(result['food2']['nutrition'].items())[:5]:
            print(f"  • {nutrient}: {value}")
        
        print("\n🔍 HASIL PERBANDINGAN:")
        print("-"*70)
        for i, comp in enumerate(result['comparison'], 1):
            print(f"  {i}. {comp}")
        
        print("\n" + "="*70)
    
    def find_high_nutrient(self, nutrient: str, min_value: float = 0):
        """Cari makanan dengan nutrient tinggi"""
        results = self.inference_engine.find_foods_by_nutrient(nutrient, min_value)
        
        if not results:
            print(f"\n❌ Tidak ada makanan dengan {nutrient} >= {min_value}")
            return
        
        print("\n" + "="*70)
        print(f"🔍 MAKANAN TINGGI {nutrient.upper()}")
        print("="*70)
        
        for i, (food, value) in enumerate(results, 1):
            print(f"  {i}. {food.capitalize():<15}: {value}")
        
        print("\n" + "="*70)
    
    def list_all_foods(self):
        """Tampilkan semua makanan dalam database"""
        print("\n" + "="*70)
        print("📋 DAFTAR MAKANAN DALAM DATABASE")
        print("="*70)
        
        for category in ['sayuran', 'buah', 'makanan']:
            foods = self.kb.get_foods_by_type(category)
            print(f"\n{category.capitalize()}:")
            for food in foods:
                print(f"  • {food}")
        
        print("\n" + "="*70)


# ===========================
# MAIN PROGRAM
# ===========================

def main():
    """Program utama sistem pakar"""
    expert_system = ExpertSystemInterface()
    
    print("\n" + "="*70)
    print("🍎 NUTRISPARK EXPERT SYSTEM")
    print("   Rule-Based Expert System dengan Forward Chaining")
    print("="*70)
    
    while True:
        print("\n📋 MENU:")
        print("  1. Analisis Nutrisi Makanan")
        print("  2. Bandingkan Dua Makanan")
        print("  3. Cari Makanan Tinggi Nutrisi Tertentu")
        print("  4. Lihat Daftar Makanan")
        print("  5. Keluar")
        
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == '1':
            food = input("Masukkan nama makanan: ").strip()
            expert_system.analyze(food)
            
        elif choice == '2':
            food1 = input("Masukkan makanan pertama: ").strip()
            food2 = input("Masukkan makanan kedua: ").strip()
            expert_system.compare(food1, food2)
            
        elif choice == '3':
            print("\nNutrisi yang tersedia: Kalori, Protein, Karbohidrat, Serat, Lemak, dll")
            nutrient = input("Masukkan nama nutrisi: ").strip()
            try:
                min_val = float(input("Masukkan nilai minimum (enter untuk 0): ").strip() or 0)
                expert_system.find_high_nutrient(nutrient, min_val)
            except ValueError:
                print("❌ Nilai tidak valid!")
                
        elif choice == '4':
            expert_system.list_all_foods()
            
        elif choice == '5':
            print("\n👋 Terima kasih telah menggunakan NutriSpark Expert System!")
            print("="*70 + "\n")
            break
            
        else:
            print("\n❌ Pilihan tidak valid!")


if __name__ == "__main__":
    main()