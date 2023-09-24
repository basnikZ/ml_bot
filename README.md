ML's projekt - myšlenková mapa

Kroky:
Sestrojit bridge mezi Metatrader4/5/IB workstation a python scriptem + získávání reálných dat v reálném čase
Vymyslet koncept výsledku strojového učení a to, jak výsledek správně využívat = strategie
Sestrojit machine learning script a jeho koncept, jakým způsobem bude data zpracovávat a jaké data bude zpracovávat pro danou strategii

Fáze:
Základní python ML skript, který bude koncentrovaný na jeden forexoví pár, zpracovávat data o něm, odesílat přes bridge brokerovi (workstation/metatrader - > broker) a uskutečňovat obchody.
Rozšíření zpracovávaných dat za cílem zakomponovat I fundamentální data pro zlepšení výsledků
Rozšíření zpracovávání dat ML skriptem na více párů a následné porovnávání a hledání shody za cílem zlepšení výsledků
Počáteční rozvržení základních úkolů mezi team:

Peťa: 
Sestavit bridge mezi python skriptem a obchodné platformou
Najít vhodný zdroj historických a aktuálních dat

Rosťa:
Vytvořit základní ML python skript, který bude umět zpracovávat data na základě neurolové sítě, indikátorů a dalších nástrojů pro výpočet ceny/trendu forexového páru

Zbyňa:
Vymyslet koncept/strategii, na základě čeho bude ML skript zpracovávat data a dávat nám žádané výsledky učení (jak často ML bude se učit, jaké hodnoty od něj chceme (ceny/trend), jak dopředu chceme, aby ML dělal forecast a jak dané výsledky využít v praxi) 
Následný backtesting finálního produktu
