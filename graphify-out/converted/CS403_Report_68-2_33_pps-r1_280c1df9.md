<!-- converted from CS403_Report_68-2_33_pps-r1.docx -->



การสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์: กรณีศึกษาจังหวัดภูเก็ต





โดย

นาย ทีมไทย น้อยสุวรรณา





โครงงานพิเศษนี้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตร
วิทยาศาสตรบัณฑิต
สาขาวิชาวิทยาการคอมพิวเตอร์ 
คณะวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยธรรมศาสตร์
ปีการศึกษา 2568
ลิขสิทธิ์ของมหาวิทยาลัยธรรมศาสตร์
การสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์: กรณีศึกษาจังหวัดภูเก็ต


โดย

นาย ทีมไทย น้อยสุวรรณา











โครงงานพิเศษนี้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตร
วิทยาศาสตรบัณฑิต
สาขาวิชาวิทยาการคอมพิวเตอร์ 
คณะวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยธรรมศาสตร์
ปีการศึกษา 2568
ลิขสิทธิ์ของมหาวิทยาลัยธรรมศาสตร์
BUDGET-AWARE TRAVEL ROUTE GENERATION AND OPTIMIZATION USING ARTIFICIAL INTELLIGENCE: A PHUKET CASE STUDY


BY

MR TEAMTHAI NOISUWANNA











A FINAL-YEAR PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE DEGREE OF BACHELOR OF SCIENCE
COMPUTER SCIENCE
FACULTY OF SCIENCE AND TECHNOLOGY
THAMMASAT UNIVERSITY
ACADEMIC YEAR 2025
COPYRIGHT OF THAMMASAT UNIVERSITY
มหาวิทยาลัยธรรมศาสตร์
คณะวิทยาศาสตร์และเทคโนโลยี

รายงานโครงงานพิเศษ

ของ

นาย ทีมไทย น้อยสุวรรณา


เรื่อง

การสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์: กรณีศึกษาจังหวัดภูเก็ต

ได้รับการตรวจสอบและอนุมัติ ให้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตร
หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์
เมื่อ วันที่ 22 พฤษภาคม พ.ศ. 2569


| อาจารย์ที่ปรึกษา | (ผู้ช่วยศาสตราจารย์ ปกป้อง ส่องเมือง) |
| --- | --- |
| กรรมการสอบโครงงานพิเศษ | (ผู้ช่วยศาสตราจารย์ ปกป้อง ส่องเมือง) |
| กรรมการสอบโครงงานพิเศษ | (ผู้ช่วยศาสตราจารย์ กษิดิศ ชาญเชี่ยว) |
| กรรมการสอบโครงงานพิเศษ | (อาจารย์ นวฤกษ์ ชลารักษ์) |

มหาวิทยาลัยธรรมศาสตร์
คณะวิทยาศาสตร์และเทคโนโลยี

รายงานโครงงานพิเศษ

ของ

นาย ทีมไทย น้อยสุวรรณา

เรื่อง

การสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์: กรณีศึกษาจังหวัดภูเก็ต

ได้รับการตรวจสอบและอนุมัติ ให้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตร
หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์
เมื่อ วันที่ 22 พฤษภาคม พ.ศ. 2569


| อาจารย์ที่ปรึกษา | (ผู้ช่วยศาสตราจารย์ ปกป้อง ส่องเมือง) |
| --- | --- |
| กรรมการสอบโครงงานพิเศษ | (ผู้ช่วยศาสตราจารย์ ปกป้อง ส่องเมือง) |
| กรรมการสอบโครงงานพิเศษ | (ผู้ช่วยศาสตราจารย์ กษิดิศ ชาญเชี่ยว) |
| กรรมการสอบโครงงานพิเศษ | (อาจารย์ นวฤกษ์ ชลารักษ์) |

| หัวข้อโครงงานพิเศษ | การสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์: กรณีศึกษาจังหวัดภูเก็ต |
| --- | --- |
| ชื่อผู้เขียน | นาย ทีมไทย น้อยสุวรรณา |
| ชื่อปริญญา | วิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์ |
| สาขาวิชา/คณะ/มหาวิทยาลัย | สาขาวิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยธรรมศาสตร์ |
| อาจารย์ที่ปรึกษาโครงงานพิเศษ | ผู้ช่วยศาสตราจารย์ ปกป้อง ส่องเมือง |
| ปีการศึกษา | 2568 |




















บทคัดย่อ

โครงงานนี้นำเสนอระบบสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์ โดยใช้จังหวัดภูเก็ตเป็นกรณีศึกษาใน Project 1 ระบบแก้ปัญหา Budget-Constrained Team Orienteering Problem with Time Windows (B-TOPTW) ด้วยอัลกอริทึม 3 แบบ ได้แก่ Greedy Algorithm (baseline), Genetic Algorithm (GA), และ Hybrid Algorithm ระบบจะสร้างแพ็กเกจแนะนำการท่องเที่ยว 3 แพ็กเกจการท่องเที่ยวอัตโนมัติ
ตามระดับงบประมาณ และอนุญาตให้ผู้ใช้ปรับแต่งสถานที่ในแต่ละวันผู้ทำได้พัฒนาฐานข้อมูลสถานที่ท่องเที่ยวในจังหวัดภูเก็ตจำนวน 164 จุด (ร้านอาหาร 49, หาด 29, วัด 24, กิจกรรม 21, วัฒนธรรม 19, จุดชมวิว 12, ตลาด 10) พร้อมโรงแรม 20 แห่ง ครอบคลุมระดับราคาประหยัด มาตรฐาน และพรีเมี่ยม โดยดึงข้อมูลจาก OpenStreetMap ผ่าน Overpass API และนำอัลกอริทึมทั้ง 3 แบบ มาใช้คำนวณเส้นทางและหาสถานที่ที่เหมาะสม ผลการทดลอง 15 รอบต่อ scenario พบว่า Hybrid Algorithm ให้ score สูงสุดในทุก scenario (S1: 152.2, S2: 247.6, S3: 347.4) เหนือกว่า Greedy (S1: 148.1, S2: 244.6, S3: 346.7) และ Genetic Algorithm อย่างมีนัยสำคัญทางสถิติ (Kruskal-Wallis p<0.001 ทุก scenario)
ผลลัพธ์ยืนยันประสิทธิภาพที่ดีกว่าของ Hybrid Algorithm ในทุกสภาวะงบประมาณ และเป็นพื้นฐานสำหรับการต่อยอดในโครงงานพิเศษ 2 ซึ่งจะมุ่งเน้น Multi-objective Optimization, Dynamic Pricing, และการขยายครอบคลุม 77 จังหวัดทั่วประเทศไทย
คำสำคัญ: การท่องเที่ยวประเทศไทย, ปัญญาประดิษฐ์, อัลกอริทึมเชิงพันธุกรรม, การจัดเส้นทางท่องเที่ยว, Team Orienteering Problem, OpenStreetMap








| Thesis Title | BUDGET-AWARE TRAVEL ROUTE GENERATION AND OPTIMIZATION USING ARTIFICIAL INTELLIGENCE: A PHUKET CASE STUDY |
| --- | --- |
| Author | MR TEAMTHAI NOISUWANNA |
| Degree | Bachelor of Science |
| Major Field/Faculty/University | Computer Science Faculty of Science and Technology Thammasat University |
| Project Advisor | ASST.PROF.DR. POKPONG SONGMUANG |
| Academic Years | 2025 |




















ABSTRACT

This project presents a system for creating and optimizing tourist routes within budget using artificial intelligence, with Phuket Province as a case study in Project 1. The system addresses the Budget-Constrained Team Orienteering Problem with Time Windows (B-TOPTW) using three algorithms: Greedy Algorithm (baseline), Genetic Algorithm (GA), and a novel Hybrid Algorithm proposed in this work. The system generates three trip packages at different budget levels and allows per-day customization.
The authors constructed a dataset of 164 points of interest in Phuket (49 restaurants, 29 beaches, 24 temples, 21 activities, 19 culture sites, 12 viewpoints, 10 markets) Data was collected from OpenStreetMap together with 20 reference hotels covering budget, standard, and premium price tiers, and implemented all three algorithms. Experiments across 15 trials per scenario show that the Hybrid Algorithm achieves the highest scores in all three scenarios (S1: 152.2, S2: 247.6, S3: 347.4) compared to Greedy (S1: 148.1, S2: 244.6, S3: 346.7) and GA, with statistically significant differences (Kruskal-Wallis p<0.001 for all scenarios).
These results confirm the superior performance of the Hybrid Algorithm across all scenarios and lay the groundwork for future enhancements in Special Project 2, including multi-objective optimization, dynamic real-time data integration, expansion to all 77 Thai provinces, and personalized AI-driven recommendations.

Keywords: Thailand Tourism, Artificial Intelligence, Genetic Algorithm, Hybrid Algorithm, Travel Route Optimization, Team Orienteering Problem, OpenStreetMap



กิตติกรรมประกาศ
ผู้จัดทำขอขอบพระคุณผู้ช่วยศาสตราจารย์ ที่ได้ให้คำแนะนำและข้อเสนอแนะอันมีค่าตลอดระยะเวลาในการพัฒนาโครงงานนี้รวมถึงคณาจารย์ในสาขาวิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยธรรมศาสตร์ที่ได้ถ่ายทอดความรู้พื้นฐานที่จำเป็น
ต่อการดำเนินโครงงานขอกราบขอบพระคุณคณะกรรมการสอบโครงงานทุกท่าน ที่ได้ให้ข้อเสนอแนะและติติงอันเป็นประโยชน์อย่างยิ่ง ซึ่งช่วยให้การพัฒนาระบบ "การสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์" สามารถตอบโจทย์กลุ่มผู้ใช้งานได้อย่างมีประสิทธิภาพและมีความสมบูรณ์มากยิ่งขึ้น
ขอขอบคุณเพื่อนนักศึกษาที่ร่วมเรียนและให้กำลังใจในระหว่างกระบวนการพัฒนา ตลอดจนครอบครัวและบุคคลใกล้ชิดที่ให้การสนับสนุนทั้งกำลังกายและกำลังใจ ทำให้โครงงานนี้สำเร็จลุล่วงไปได้ด้วยดี

นาย ทีมไทย น้อยสุวรรณา












สารบัญ

หน้า
บทคัดย่อ	2
ABSTRACT	4
กิตติกรรมประกาศ	5
สารบัญ	6
สารบัญตาราง	9
ตารางที่ 4.1 ผลการทดลองเปรียบเทียบประสิทธิภาพ 3 อัลกอริทึม (Mean Score ± Std, 15 trials)	12	9
ตารางที่ 4.2 การดำเนินงานที่ผ่านมาจนถึงปัจจุบัน	16	9
ตารางที่ 4.3 แผนการดำเนินงานในอนาคต	16	9
สารบัญภาพ	10
รายการสัญลักษณ์และคำย่อ	11
บทที่ 1	12
1.1	ความเป็นมาและความสำคัญของโครงงาน	12
1.2	วัตถุประสงค์	12
1.3	ขอบเขตของโครงงาน	13
1.4	ประโยชน์ของโครงงาน	14
1.5	ข้อจำกัดของโครงงาน	15
บทที่ 2	วรรณกรรมและงานวิจัยที่เกี่ยวข้อง	16
2.1	แนวคิดทฤษฎีที่เกี่ยวข้อง	16
2.1.1	Orienteering Problem (OP)	16
2.1.2	Team Orienteering Problem with Time Windows (TOPTW)	16
2.1.3	Genetic Algorithm (GA)	16
2.1.4	Greedy Algorithm	16
2.2	งานวิจัยที่เกี่ยวข้อง	17
2.2.1	งานวิจัยของ Vansteenwegen และคณะ (2009)	17
2.2.2	งานวิจัยของ Gavalas และคณะ (2014)	17
2.2.3	งานวิจัยของ Souffriau และคณะ (2008)	17
2.2.4	ความแตกต่างของโครงงานนี้กับงานวิจัยข้างต้น	17
บทที่ 3	วิธีการวิจัย	18
3.1	ภาพรวมของโครงงาน	18
3.1.1	Workflow การใช้งาน	18
3.1.2	สถาปัตยกรรมของระบบ	18
3.1.3	การจัดสรรงบประมาณตาม Tier	18
3.2	การวิเคราะห์ขอบเขตและความต้องการของระบบ	19
3.3	ประเด็นที่น่าสนใจและสิ่งที่ท้าทาย	19
3.3.1	การออกแบบ Chromosome Representation	19
3.3.2	การจัดการ Constraint Violation	19
3.3.3	การปรับสมดุลระหว่าง Exploration และ Exploitation	20
3.3.4	การออกแบบ Schedule ให้สมจริง (Realistic Schedule Design)	20
3.3.5	Hybrid Algorithm	20
3.3.6	Free-Attraction Fallback Mechanism (สำคัญสำหรับงบจำกัด)	21
3.3.7	Forced Meal-Time Wait	21
3.3.8	Algorithm Selector ใน Frontend	21
3.3.9	การออกแบบ UX สำหรับการสำรวจเส้นทางหลายวัน	22
3.4	ผลลัพธ์ที่คาดหวัง	22
3.5	ระบบต้นแบบและผลลัพธ์เบื้องต้น	22
บทที่ 4	ทรัพยากรและแผนการดำเนินงาน	25
4.1	การจัดเตรียมฮาร์ดแวร์และซอฟต์แวร์	25
4.1.1	ฮาร์ดแวร์	25
4.1.2	ซอฟต์แวร์และเครื่องมือ	25
4.2	แผนการดำเนินงาน	25
บทที่ 5	สรุป	28
รายการอ้างอิง	29
ภาคผนวก	30
ภาคผนวก ก ภาพหน้าจอระบบ WeEasyTrip	30
ภาคผนวก ข ผลการทดลองแบบละเอียดทุก Trial	33
ภาคผนวก ค ตัวอย่างโครงสร้างข้อมูล POI และโรงแรม	36






สารบัญตาราง

หน้า
ตารางที่ 4.1 ผลการทดลองเปรียบเทียบประสิทธิภาพ 3 อัลกอริทึม (Mean Score ± Std, 15 trials)	12
ตารางที่ 4.2 การดำเนินงานที่ผ่านมาจนถึงปัจจุบัน	16
ตารางที่ 4.3 แผนการดำเนินงานในอนาคต	16
ตาราง ข.1 ผลทุก Trial — Scenario 1 (3 วัน, งบ 10,000 บาท)	32
ตาราง ข.2 ผลทุก Trial — Scenario 2 (5 วัน, งบ 15,000 บาท)	32
ตาราง ข.3 ผลทุก Trial — Scenario 3 (7 วัน, งบ 25,000 บาท)	33
ตาราง ค.1 โครงสร้างฟิลด์ของข้อมูล POI	35
ตาราง ค.2 ตัวอย่างข้อมูล POI จากฐานข้อมูล	35
ตาราง ค.3 ตัวอย่างข้อมูลโรงแรมทั้ง 3 ระดับ	36

สารบัญภาพ
หน้า
รูปที่ 4.1 กราฟ Convergence ของ GA และ Hybrid Algorithm ทั้ง 3 Scenarios	12
รูปที่ ก.1 หน้าหลักและฟอร์มกรอกข้อมูลของระบบ WeEasyTrip	31
รูปที่ ก.2 หน้าแสดงผล 3 แพ็กเกจ (Budget / Standard / Premium)	31
รูปที่ ก.3 หน้ารายละเอียดแพ็กเกจและแผนที่เส้นทาง	32
รูปที่ ก.4 หน้าต่างการเปลี่ยนสถานที่ (Swap Modal)	32
รูปที่ ก.5 กราฟ Convergence ของ GA และ Hybrid Algorithm ทั้ง 3 Scenarios	32


















รายการสัญลักษณ์และคำย่อ

| สัญลักษณ์/คำย่อ | คำเต็ม/คำจำกัดความ |
| --- | --- |
| AI B-TOPTW TOPTW GA TOP POI NP-hard OSM API S1, S2, S3 FastAPI UI | Artificial Intelligence (ปัญญาประดิษฐ์) Budget-Constrained Team Orienteering Problem with Time Windows Team Orienteering Problem with Time Windows Genetic Algorithm (อัลกอริทึมเชิงพันธุกรรม) Team Orienteering Problem Point of Interest (จุดสนใจ/สถานที่ท่องเที่ยว) Non-deterministic Polynomial-time hard OpenStreetMap Application Programming Interface Scenario 1, 2, 3 (สถานการณ์ทดสอบที่ 1, 2, 3) Framework สำหรับพัฒนา Web API ด้วย Python User Interface (ส่วนติดต่อผู้ใช้) |


บทนำ
## ความเป็นมาและความสำคัญของโครงงาน
การท่องเที่ยวเป็นกิจกรรมที่ได้รับความนิยมอย่างแพร่หลายในปัจจุบัน อย่างไรก็ตาม กระบวนการวางแผนการท่องเที่ยวนั้นมีความซับซ้อนและใช้เวลาอย่างมาก นักท่องเที่ยวจำเป็นต้องค้นหาข้อมูลสถานที่ท่องเที่ยวจากแหล่งข้อมูลหลายแห่งพร้อมกัน ไม่ว่าจะเป็นเว็บไซต์รีวิว แอปพลิเคชันแผนที่ แพลตฟอร์มจองที่พัก หรือช่องทางโซเชียลมีเดียต่าง ๆ การรวบรวมและเปรียบเทียบข้อมูลจากหลายแหล่งดังกล่าวทำให้นักท่องเที่ยวต้องเสียเวลาและความพยายามอย่างมาก
ปัจจุบันแม้จะมีระบบแนะนำการท่องเที่ยวอยู่หลายระบบ แต่ส่วนใหญ่จะแสดงผลเป็นรายการสถานที่แยกจากกัน หรือจัดเส้นทางโดยอ้างอิงเฉพาะระยะทางทางภูมิศาสตร์เท่านั้น ไม่ได้คำนึงถึงข้อจำกัดหลายมิติพร้อมกัน เช่น งบประมาณรวมของผู้ใช้ ช่วงเวลาเปิด-ปิดของแต่ละสถานที่ ระยะเวลาที่ใช้ในแต่ละจุด การจัดมื้ออาหารระหว่างวันให้สมจริง และการเริ่มต้น-สิ้นสุดที่โรงแรม ทำให้ผู้ใช้ต้องวางแผนต่อด้วยตนเอง
ในเชิงทฤษฎี ปัญหาดังกล่าวจัดอยู่ในกลุ่ม Team Orienteering Problem with Time Windows (TOPTW) ภายใต้ข้อจำกัดด้านงบประมาณ ซึ่งเป็นปัญหา NP-hard ไม่สามารถแก้ด้วย exact algorithm ได้ในเวลาที่ยอมรับได้เมื่อจำนวนสถานที่เพิ่มขึ้น จึงต้องอาศัย metaheuristic เช่น Genetic Algorithm (GA), Simulated Annealing (SA), หรือ Ant Colony Optimization (ACO) เพื่อให้ได้คำตอบที่มีคุณภาพดีในเวลาที่เหมาะสม
โครงงานนี้นำเสนอระบบสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์ โดยขอบเขตใน Project 1 ใช้จังหวัดภูเก็ตเป็นกรณีศึกษาเพื่อพิสูจน์ความเป็นไปได้ของระบบ ระบบที่ออกแบบรองรับการขยายไปยังจังหวัดอื่นทั่วประเทศไทยในระยะ Project 2 โดยเปรียบเทียบประสิทธิภาพของ 3 อัลกอริทึม ได้แก่ Greedy Algorithm (baseline), Genetic Algorithm, และ Hybrid Algorithm เพื่อยืนยันว่า Hybrid Algorithm ให้ผลลัพธ์ที่ดีกว่าทั้งในเชิงคุณภาพของคำตอบและความสามารถในการรองรับ constraint หลายข้อพร้อมกัน
## วัตถุประสงค์
โครงงานนี้มีเป้าหมายเพื่อพัฒนาระบบต้นแบบที่สร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณที่ผู้ใช้กำหนด โดยประยุกต์ใช้เทคนิคปัญญาประดิษฐ์หลายแบบ ได้แก่ Greedy Algorithm, Genetic Algorithm, และ Hybrid Algorithm โดยใน Project 1 ใช้จังหวัดภูเก็ตเป็นกรณีศึกษา เพื่อให้บรรลุเป้าหมายดังกล่าว จึงกำหนดวัตถุประสงค์ของโครงงานดังต่อไปนี้
1. นิยามปัญหา Budget-Constrained Team Orienteering Problem with Time Windows (B-TOPTW) ในเชิงคณิตศาสตร์ ที่ครอบคลุมข้อจำกัดด้านงบประมาณ เวลาเปิด-ปิดของสถานที่ ระยะเวลาในแต่ละจุด และการเริ่มต้น-สิ้นสุดที่โรงแรม
2. พัฒนาระบบต้นแบบที่ใช้ Genetic Algorithm ในการแก้ปัญหา B-TOPTW โดยรองรับการสร้าง 3 packages อัตโนมัติ (Budget / Standard / Premium) ตามระดับงบประมาณ
3. พัฒนาฟังก์ชัน custom package ที่ให้ผู้ใช้สามารถเปลี่ยนสถานที่ในแต่ละวันได้ และระบบทำการ re-optimize เส้นทางและคำนวณค่าใช้จ่ายใหม่แบบอัตโนมัติ
4. ทดสอบและเปรียบเทียบประสิทธิภาพของ 3 อัลกอริทึม คือ Greedy Algorithm (baseline), Genetic Algorithm, และ Hybrid Algorithm (ที่นำเสนอใหม่ในโครงงาน) บนชุดข้อมูลสถานที่ท่องเที่ยวในจังหวัดภูเก็ต โดยวัดทั้งคุณภาพคำตอบ (total score), เวลาที่ใช้ (runtime), และความสมจริงของ schedule (days with POIs)
5. พัฒนาเว็บไซต์ที่นำเสนอระบบในรูปแบบที่ใช้งานได้จริง โดยแสดงเส้นทางบนแผนที่และตารางค่าใช้จ่ายอย่างชัดเจน
## ขอบเขตของโครงงาน
โครงงานนี้กำหนดขอบเขตการพัฒนาและการทดสอบไว้ดังนี้
1. ขอบเขตหลักของระบบครอบคลุมการท่องเที่ยวในประเทศไทย โดยใน Project 1 (ฉบับนี้) จำกัดการทดสอบที่จังหวัดภูเก็ตเป็น case study ใช้ฐานข้อมูลสถานที่ท่องเที่ยว 164 จุด (ร้านอาหาร 49, หาด 29, วัด 24, กิจกรรม 21, วัฒนธรรม 19, จุดชมวิว 12, ตลาด 10) และโรงแรม 20 แห่งในรูปแบบ static dataset ดึงจาก OpenStreetMap frontend และใน Project 2 จะขยายไปยังจังหวัดอื่นๆ
2. ระยะเวลาทริปที่ระบบรองรับอยู่ที่ 1-7 วัน โดยทุกวันเริ่มและสิ้นสุดที่โรงแรมเดียวกัน และยังรวมถึงการท่องเที่ยวแบบ One-day trip
3. งบประมาณที่ระบบรองรับอยู่ในช่วง 1000 - 100,000 บาทต่อทริป (ครอบคลุม day-trip ราคาถูกถึงทริปหรู)
4. อัลกอริทึมที่นำมาเปรียบเทียบมี 3 ตัว ได้แก่ Greedy Algorithm (baseline, slot-based), Genetic Algorithm (population-based metaheuristic), และ Hybrid Algorithm (Greedy seed + GA refinement + 2-opt local search ที่นำเสนอใหม่ในโครงงาน) ผู้ใช้สามารถสลับ algorithm ได้จาก UI เพื่อเปรียบเทียบผลลัพธ์
5. ระบบเป็นแบบ web-based ที่ใช้งานบน browser ทั่วไป โดยใช้ Python (FastAPI) เป็น backend และ HTML/JavaScript กับ Leaflet.js เป็น frontend
6. โครงงานนี้ไม่ครอบคลุมการดึงข้อมูลแบบ real-time จาก Google Maps หรือ TripAdvisor การจองโรงแรม-ตั๋วทัวร์ การคิดค่าเดินทางตามสภาพการจราจรจริง การ login ของผู้ใช้ และการแจ้งเตือนสภาพอากาศ
## ประโยชน์ของโครงงาน
ระบบที่พัฒนาขึ้นในโครงงานนี้ก่อให้เกิดประโยชน์ในหลายด้าน ดังนี้
ในด้านวิชาการ โครงงานนำเสนอกรณีศึกษาเชิงประยุกต์ของ Genetic Algorithm กับปัญหา TOPTW ที่มี budget constraint เพิ่มเติม รวมถึง realistic schedule constraints (มื้ออาหารตามช่วงเวลาจริง, ความหลากหลายของหมวดสถานที่) ซึ่งสามารถใช้เป็นพื้นฐานในการต่อยอดงานวิจัยด้าน Tourist Trip Design Problem (TTDP) ในบริบทของประเทศไทยได้
ในด้านการประยุกต์ใช้งาน นักท่องเที่ยวที่วางแผนทริปในประเทศไทยสามารถใช้ระบบเพื่อรับคำแนะนำเส้นทางและค่าใช้จ่ายโดยประมาณภายในเวลาไม่กี่วินาที ลดเวลาในการค้นข้อมูลและจัดตารางทริปด้วยตนเอง โดยในระยะ Project 1 ครอบคลุมจังหวัดภูเก็ต และระยะ Project 2 จะขยายไปยังทุกจังหวัดทั่วประเทศ
ในด้านการต่อยอดเทคโนโลยี ระบบวางรากฐานสำหรับการประยุกต์ใช้ Generative AI ใน Project 2 ทั้งการดึงข้อมูล real-time (ราคาโรงแรม ค่าเข้าสถานที่ พยากรณ์อากาศ)
ในด้านการเรียนการสอน source code และ dataset ของโครงงานสามารถใช้เป็นตัวอย่างประกอบการเรียนวิชาที่เกี่ยวข้องกับ Optimization, Metaheuristics, และ Algorithm Analysis ในระดับปริญญาตรี


## ข้อจำกัดของโครงงาน
โครงงานนี้มีข้อจำกัดที่ผู้ใช้และผู้พัฒนาต่อยอดควรทราบดังนี้
1. ฐานข้อมูลสถานที่ท่องเที่ยวเป็น static dataset ที่จัดเตรียมไว้ล่วงหน้า ไม่ได้อัปเดตตามข้อมูลจริงแบบเรียลไทม์ ค่าใช้จ่ายและช่วงเวลาเปิด-ปิดอาจเปลี่ยนแปลงตามฤดูกาล
2. ระยะทางและเวลาเดินทางระหว่างจุด คำนวณจากระยะทาง haversine (เส้นตรงระหว่างพิกัด) คูณด้วยตัวคูณค่าคงที่ ไม่ได้ใช้ข้อมูลถนนหรือสภาพการจราจรจริง
















# วรรณกรรมและงานวิจัยที่เกี่ยวข้อง

## แนวคิดทฤษฎีที่เกี่ยวข้อง
ส่วนนี้นำเสนอแนวคิดทฤษฎีพื้นฐานที่เกี่ยวข้องกับโครงงาน ครอบคลุมปัญหาการจัดเส้นทาง อัลกอริทึมเชิงพันธุกรรม และการประเมินคุณภาพของคำตอบในปัญหา NP-hard
### Orienteering Problem (OP)
ปัญหา OP คือปัญหาการเลือก subset ของจุดบนกราฟ พร้อมจัดลำดับการเดินทาง โดยที่ผลรวมของ score (รางวัล) ของจุดที่เลือกสูงสุด ภายใต้ข้อจำกัดด้านระยะเวลา OP เป็นการ generalize ปัญหา Traveling Salesman Problem (TSP) ที่อนุญาตให้ไม่ต้องเดินทางผ่านทุกจุด ปัญหานี้ถูกพิสูจน์ว่าเป็น NP-hard ทำให้การแก้ด้วย exact algorithm ใช้เวลามากเมื่อจำนวนจุดเพิ่มขึ้น
### Team Orienteering Problem with Time Windows (TOPTW)
TOPTW เป็นการขยายปัญหา OP ใน 2 ทิศทาง คือ
(1) มีหลายเส้นทาง (team) ทำให้สามารถใช้แทนทริปหลายวันได้
(2) แต่ละจุดมีช่วงเวลาที่อนุญาตให้เข้าถึง (time window) เพิ่ม constraint ทำให้ปัญหาซับซ้อนขึ้น เหมาะสำหรับโจทย์การท่องเที่ยวที่สถานที่แต่ละแห่งมีเวลาเปิด-ปิดต่างกัน
### Genetic Algorithm (GA)
GA เป็น metaheuristic แบบ population-based ที่จำลองกระบวนการคัดเลือกตามธรรมชาติ ทำงานโดยรักษากลุ่มของคำตอบ (population) แล้วปรับปรุงคำตอบในแต่ละ generation ผ่าน 3 operator หลัก ได้แก่ Selection (คัดเลือก parent ที่ fitness ดี), Crossover (รวมยีนของ parent สองตัว), และ Mutation (สุ่มเปลี่ยนแปลงยีนเล็กน้อย) GA เหมาะกับปัญหา NP-hard ที่ search space ใหญ่ เพราะสามารถสำรวจ space ได้แบบขนานและไม่ติดกับ local optima ได้ง่ายเหมือน gradient-based methods
### Greedy Algorithm
Greedy Algorithm คือวิธีการแก้ปัญหาที่เลือกตัวเลือกที่ดีที่สุดในแต่ละขั้นตอน (locally optimal) โดยหวังว่าจะได้คำตอบที่ดีในภาพรวม ในโครงงานนี้ใช้ Greedy เป็น baseline สำหรับเปรียบเทียบกับ GA โดยเลือกจุดที่มี ratio ของ score ต่อ cost สูงสุดเสมอ Greedy มีข้อดีที่เร็วและ implement ง่าย แต่มักให้คำตอบที่ไม่ optimal เมื่อปัญหามี constraint หลายข้อ
## งานวิจัยที่เกี่ยวข้อง
### งานวิจัยของ Vansteenwegen และคณะ (2009)
Vansteenwegen et al. (2009) ทำ survey อย่างครอบคลุมเกี่ยวกับ Orienteering Problem และนำเสนอกรอบการจำแนกประเภทของปัญหาตาม constraint ที่เพิ่มเข้ามา รวมถึงอัลกอริทึมหลักที่ใช้ในการแก้ ตั้งแต่ exact algorithm จนถึง metaheuristic งานชิ้นนี้เป็นจุดอ้างอิงสำคัญในการนิยามปัญหาของโครงงาน
### งานวิจัยของ Gavalas และคณะ (2014)
Gavalas et al. (2014) นำเสนอ survey ที่มุ่งเน้นเฉพาะ algorithmic approach สำหรับ Tourist Trip Design Problem (TTDP) ซึ่งเป็นการประยุกต์ OP ในบริบทการท่องเที่ยว งานวิจัยชี้ว่า GA และ Tabu Search เป็น metaheuristic ที่ได้รับความนิยมมากที่สุดสำหรับ TTDP เนื่องจากความยืดหยุ่นในการรองรับ constraint หลายชนิด
### งานวิจัยของ Souffriau และคณะ (2008)
Souffriau et al. (2008) นำเสนอ Greedy Randomised Adaptive Search Procedure (GRASP) สำหรับ Team Orienteering Problem ผลการทดลองบน benchmark dataset ชี้ว่า GRASP สามารถให้คำตอบที่ใกล้เคียง optimal ในเวลาที่สั้นกว่า exact algorithm มาก งานนี้เป็นแรงบันดาลใจให้โครงงานเลือกใช้ metaheuristic
### ความแตกต่างของโครงงานนี้กับงานวิจัยข้างต้น
แม้งานวิจัยข้างต้นจะครอบคลุมการแก้ปัญหา OP/TOPTW อย่างกว้างขวาง แต่ส่วนใหญ่ใช้ benchmark dataset สังเคราะห์และไม่ได้นำเสนอในรูปแบบของระบบที่ใช้งานได้จริง โครงงานนี้แตกต่างใน 2 จุด คือ
(1) ใช้ข้อมูลสถานที่ท่องเที่ยวจริงในจังหวัดภูเก็ต
(2) เพิ่ม budget constraint ที่ครอบคลุมทั้งค่าเข้าและค่าเดินทาง ซึ่งใกล้เคียงกับการใช้งานจริงของนักท่องเที่ยว


# วิธีการวิจัย

## ภาพรวมของโครงงาน
ระบบที่พัฒนาขึ้นในโครงงานนี้ประกอบด้วย 3 ส่วนหลัก ได้แก่
(1) Algorithm Engine ที่ implement ด้วย Python ทำหน้าที่แก้ปัญหา
B-TOPTW
(2) Backend API ที่ใช้ FastAPI เป็นตัวกลางระหว่าง engine กับ frontend
(3) Frontend ที่เป็น web application แสดงผลบน Leaflet.js map
### Workflow การใช้งาน
ผู้ใช้กรอกงบประมาณ จำนวนวันทริป จำนวนคน และการรวมค่าใช้จ่ายโรงแรมในงบ จากนั้นระบบส่งคำขอไปที่ backend ซึ่งเรียก Algorithm Engine ให้รัน Genetic Algorithm 3 รอบด้วยงบที่ต่างกัน (Budget / Standard / Premium) ผลลัพธ์ส่งกลับเป็น 3 packages frontend แสดงเส้นทางบนแผนที่และตารางค่าใช้จ่ายของแต่ละ package ผู้ใช้สามารถเลือก swap จุดในแต่ละวันเพื่อ re-optimize ได้
### สถาปัตยกรรมของระบบ
ระบบใช้ architecture แบบ client-server ที่ frontend และ backend สื่อสารผ่าน RESTful API การแยก algorithm engine ออกจาก API ทำให้สามารถเปลี่ยนหรือเพิ่ม algorithm อื่นได้ง่ายในอนาคต โดยไม่ต้องแก้ frontend
### การจัดสรรงบประมาณตาม Tier
ระบบใช้กลยุทธ์ tier-based budget allocation เพื่อกระจายงบประมาณระหว่างค่าโรงแรมและค่ากิจกรรมอย่างสมเหตุสมผล โดยกำหนดเพดานสัดส่วนของงบรวมที่จะใช้กับค่าโรงแรมในแต่ละ tier ดังนี้ Budget tier (โรงแรม ≤ 25% + ใช้รวม ≤ 50% ของงบ เซฟเงินครึ่งงบ), Standard tier (โรงแรม ≤ 50% + ใช้รวม ≤ 80%), Premium tier (โรงแรม ≤ 70% + ใช้รวม ≤ 100% ของงบ ใช้เต็มงบ) นอกจากนั้น Premium tier ยังใช้ scoring mode แบบ quality (พิจารณา score เป็นหลัก ไม่สนราคา) ขณะที่ Budget และ Standard ใช้ scoring mode แบบ ratio (score/cost) วิธีนี้ทำให้ Budget tier เลือกที่เที่ยวคุ้มราคา ขณะที่ Premium เลือกที่ดีที่สุดโดยไม่กังวลราคา
## การวิเคราะห์ขอบเขตและความต้องการของระบบ
จากการวิเคราะห์ความต้องการของผู้ใช้และข้อจำกัดของโครงงาน สามารถสรุปความต้องการของระบบได้ดังนี้
ความต้องการเชิงฟังก์ชัน (Functional Requirements) ประกอบด้วย
(1) ระบบต้องสามารถรับ input จากผู้ใช้ ได้แก่ งบประมาณรวม จำนวนวัน จำนวนคน และการรวมงบโรงแรมไว้ในงบประมาณ
(2) ระบบต้องสร้าง 3 packages ที่แตกต่างกันตามระดับงบประมาณ
(3) แต่ละ package ต้องแสดงเส้นทางบนแผนที่ พร้อมตารางค่าใช้จ่ายและ score รวม
(4) ระบบต้องอนุญาตให้ผู้ใช้เปลี่ยนสถานที่ในแต่ละวัน และคำนวณ route + cost ใหม่อัตโนมัติ
ความต้องการที่ไม่ใช่เชิงฟังก์ชัน (Non-Functional Requirements) ได้แก่
(1) เวลาตอบสนองในการสร้าง package ต้องไม่เกิน 10 วินาที สำหรับ N=40 จุด
(2) เวลา re-optimize เมื่อ swap จุดต้องไม่เกิน 1 วินาที
(3) UI ต้องใช้งานง่าย รองรับการดูบน desktop browser อย่างน้อย
## ประเด็นที่น่าสนใจและสิ่งที่ท้าทาย
ในการพัฒนาระบบนี้พบประเด็นและความท้าทายที่น่าสนใจหลายประการ ซึ่งจะกล่าวถึงในรายละเอียดในส่วนต่อไปนี้
### การออกแบบ Chromosome Representation
เนื่องจากปัญหาเป็น multi-day การออกแบบ chromosome ต้องสามารถแทนทริปหลายวันที่มีจำนวนจุดต่างกันในแต่ละวันได้ โครงงานนี้เลือกใช้ list of lists โดยแต่ละ inner list คือ sequence ของ POI index ในแต่ละวัน วิธีนี้ทำให้ crossover และ mutation operator มีความซับซ้อนขึ้น เพราะต้องระวังการเปลี่ยนแปลงข้ามวัน
### การจัดการ Constraint Violation
ปัญหา B-TOPTW มี constraint หลายชั้น (งบ, เวลาต่อวัน, time window) การ encode constraint เป็น hard constraint ทำให้ search space แคบเกินไป โครงงานนี้จึงใช้ soft constraint ผ่าน penalty function โดย fitness = total_score - penalty(constraint violations) เพื่อให้ GA ค้นหาคำตอบได้กว้างขึ้น
### การปรับสมดุลระหว่าง Exploration และ Exploitation
ใน GA การกำหนดค่า mutation rate และ crossover rate มีผลต่อความสามารถของอัลกอริทึมในการสำรวจ search space (exploration) เทียบกับการปรับปรุงคำตอบที่ดีอยู่แล้ว (exploitation) โครงงานจะทดสอบหลายชุดค่าเพื่อหาค่าที่เหมาะสมกับขนาดของปัญหา
### การออกแบบ Schedule ให้สมจริง (Realistic Schedule Design)
เพื่อให้แพ็กเกจที่ระบบสร้างสะท้อนรูปแบบการท่องเที่ยวจริง โครงงานเพิ่มข้อจำกัดเชิง schedule constraints ดังนี้
(1) จำกัดร้านอาหารไม่เกิน 2 ร้านต่อวัน คือ 1 มื้อกลางวัน และ 1 มื้อเย็น
(2) ระบบบังคับเลือกร้านอาหารโดยอัตโนมัติเมื่อเวลาเข้าสู่ช่วง lunch trigger (11:30) หากยังไม่ได้กิน และ dinner trigger (17:00)
(3) ห้ามเลือกร้านอาหาร 2 ร้านติดกัน หลังเลือกร้านมื้อแรก ระบบจะปฏิเสธการเลือกร้านอีกจนกว่าจะถึง dinner trigger เพื่อบังคับให้มีกิจกรรมคั่นระหว่างมื้อ ตามพฤติกรรมการท่องเที่ยวจริง
(4) ร้านอาหารร้านแรกในวันต้องมาถึงในช่วง 10:00-17:00 (lunch arrive window) ร้านที่สองอยู่ใน 17:00-22:00 (dinner arrive window) (4) แต่ละวันต้องมีจุดท่องเที่ยวอย่างน้อย 2 จุด
(5) เพิ่ม diversity bonus ให้กับ POI ในหมวดที่ยังไม่มีในวันนั้น เพื่อกระจายชนิดสถานที่
(6) per-day budget cap (1.8x average) เพื่อกระจายงบข้ามวัน ป้องกันวันแรกใช้งบหมด ใน Greedy Algorithm ใช้เป็น hard constraint ใน Genetic Algorithm ใช้เป็น soft constraint ผ่าน penalty function
### Hybrid Algorithm
เนื่องจาก Greedy Algorithm มีข้อจำกัดเชิง locally optimal (เลือกจุดดีที่สุดทีละขั้นโดยไม่คิดถึงวันถัดไป) ทำให้วันท้ายๆ ของทริปยาวมักขาดสถานที่ท่องเที่ยว ส่วน Genetic Algorithm แม้จะให้ผลลัพธ์ดีในเชิง global optimization แต่ใช้เวลามาก (2-4 วินาทีต่อการเรียก) และโครงสร้างวันไม่แน่นอน โครงงานจึงนำเสนอ Hybrid Algorithm ที่รวมข้อดีของทั้งสองวิธี ดังนี้
(1) Greedy Seeding: ใช้ Greedy slot-based สร้าง initial population โดยใช้ multiple greedy starts (สลับลำดับ POI) เพื่อความหลากหลาย
(2) GA Refinement: ใช้ GA evolve population ด้วย operator ที่ออกแบบให้รักษา slot pattern (slot_repair function) มี adaptive mutation rate (ค่าลดลงตามจำนวน generation) และ early stopping (หยุดถ้าไม่มี improvement 15 generations)
(3) 2-opt Local Search: หลัง GA จบ ใช้ 2-opt swap optimize ลำดับ attractions ในแต่ละวันเพื่อลด travel distance โดยรักษาตำแหน่ง slot 3 (lunch) และ slot 6 (dinner) ไว้
Hybrid Algorithm ทำงานในเวลาประมาณ 100-150 มิลลิวินาที (เร็วกว่า GA pure ประมาณ 20 เท่า) แต่ให้ structured output ที่สมจริงเหมือน Greedy slot-based เหมาะสำหรับใช้ใน production system ที่ต้องการทั้งคุณภาพและความเร็วในการตอบสนอง
### Free-Attraction Fallback Mechanism (สำคัญสำหรับงบจำกัด)
เพื่อรองรับนักท่องเที่ยวงบประมาณจำกัด (เริ่มต้นที่ 1000 บาท) ระบบเพิ่ม fallback 4-tier ที่ทำให้ทุกวันมีกิจกรรมแม้งบหมด ดังนี้ Try 1: หา POI ปกติในงบ → Try 2: หา POI ฟรีหมวดเดิม → Try 3: หา POI ฟรีหมวดอื่น (สำหรับ slot ร้านอาหาร) → Try 4: หา POI ที่อยู่ในงบ ไม่จำกัดหมวด ผลลัพธ์คือผู้ใช้ที่งบ 1,000 บาท สำหรับ 4 วัน ก็ยังได้ทุกวันมี 6 จุดเที่ยวครบ (เน้นจุดฟรี เช่น หาด วัด จุดชมวิว เมืองเก่า)
### Forced Meal-Time Wait
ระบบบังคับให้รอจนถึงเวลามื้ออาหาร: เมื่อถึง slot 3 (lunch) ถ้า current_time < 11:30 ระบบจะ skip ไปเป็น 11:30 ก่อนหา restaurant; เมื่อถึง slot 6 (dinner) ถ้า current_time < 17:00 ก็ skip ไปเป็น 17:00 วิธีนี้รับประกันว่าทุกวันจะมี 1 lunch + 1 dinner restaurant ในเวลาที่ถูกต้อง สมจริงตามตารางการท่องเที่ยวจริง
### Algorithm Selector ใน Frontend
เพื่อรองรับการเปรียบเทียบ ระบบมี algorithm selector ที่ให้สลับ 3 algorithm ได้ทันที (Greedy / GA / Hybrid) เป็น feature สำหรับให้กรรมการสามารถทดลองเปรียบเทียบ algorithm ได้แบบ real-time
### การออกแบบ UX สำหรับการสำรวจเส้นทางหลายวัน
เนื่องจากเส้นทางหลายวันมี marker จำนวนมากบนแผนที่เดียวกัน ระบบจึงเพิ่มฟีเจอร์ day filter ที่ผู้ใช้สามารถเปิด-ปิดการแสดงผลของแต่ละวันได้แยกกัน ทำให้สามารถวิเคราะห์เส้นทางทีละวันได้โดยไม่สับสน
## ผลลัพธ์ที่คาดหวัง
ผลลัพธ์ที่ได้จากโครงงานพิเศษ 1 ประกอบด้วย
1. ระบบต้นแบบที่ใช้งานได้จริงผ่าน web browser โดยมีฟีเจอร์ครบตามขอบเขตที่กำหนด
2. รายงานเปรียบเทียบประสิทธิภาพของ 3 อัลกอริทึม (Greedy / GA / Hybrid) ด้วย 135 trials บนชุดข้อมูลภูเก็ต 164 จุด ผลจริง: Hybrid ให้ score สูงสุดทุก scenario (S1=152.2, S2=247.5, S3=347.4) เหนือกว่า Greedy (S1=148.1, S2=244.6, S3=346.7) อย่างมีนัยสำคัญ (Kruskal-Wallis p<0.001) GA ใช้เวลา 430-880 ms, Hybrid 120-270 ms, Greedy 8-18 ms
3. กราฟ convergence ของ GA และ Hybrid Algorithm ที่แสดงให้เห็นการปรับปรุงคำตอบในแต่ละ generation ครบทั้ง 3 scenarios
## ระบบต้นแบบและผลลัพธ์เบื้องต้น
ผู้จัดทำได้สร้างต้นแบบเบื้องต้นที่ครอบคลุม
(1) ฐานข้อมูลสถานที่ท่องเที่ยวภูเก็ต 164 จุด (ร้านอาหาร 49, หาด 29, วัด 24, กิจกรรม 21, วัฒนธรรม 19, จุดชมวิว 12, ตลาด 10) พร้อมโรงแรม 20 แห่ง ดึงจาก OpenStreetMap ผ่าน Overpass API ในรูปแบบ JSON พร้อม metadata ครบถ้วน
(2) Greedy slot-based Algorithm ที่บังคับ Day Pattern (attr-attr-lunch-attr-attr-dinner) ทุกวัน
(3) Genetic Algorithm พร้อม greedy seeding, tournament selection, day-level crossover, และ slot-aware mutation
(4) Hybrid Algorithm ที่รวม Greedy seed + GA refinement + 2-opt local search
(5) Backend API ผ่าน FastAPI ที่ expose 3 endpoints คือ /api/health, /api/packages, และ /api/recompute
ผลการทดลองครบถ้วนด้วยชุดข้อมูล 164 จุด + 20 โรงแรม แบ่ง 3 scenarios (S1: 10,000 บาท 3 วัน, S2: 15,000 บาท 5 วัน, S3: 25,000 บาท 7 วัน) จำนวน 15 รอบต่อ scenario รวม 135 trials พบว่า: Hybrid Algorithm ให้ score สูงสุดทุก scenario ได้แก่ S1=152.2, S2=247.5, S3=347.4 เหนือกว่า Greedy (S1=148.1, S2=244.6, S3=346.7) และ Genetic Algorithm (S1=148.5, S2=244.4, S3=332.12) อย่างมีนัยสำคัญทางสถิติด้วย Kruskal-Wallis test (p<0.001 ทุก scenario) Greedy Algorithm รันใน 8-18 มิลลิวินาที, Hybrid Algorithm ใช้เวลา 120-270 มิลลิวินาที ทุกวันมี Day Pattern ครบ (attr-attr-lunch-attr-attr-dinner) ผลลัพธ์ยืนยันความเหนือกว่าของ Hybrid Algorithm ในทุกสภาวะงบประมาณ
ตารางที่ 4.1 ผลการทดลองเปรียบเทียบประสิทธิภาพ 3 อัลกอริทึม (Mean Score ± Std, 15 trials)
| อัลกอริทึม | S1: 3วัน / 10,000฿ | S2: 5วัน / 15,000฿ | S3: 7วัน / 25,000฿ |
| --- | --- | --- | --- |
| Greedy Algorithm | 148.10 ± 0.00 | 244.60 ± 0.00 | 346.70 ± 0.00 |
| Genetic Algorithm (GA) | 147.51 ± 3.23 | 244.49 ± 1.59 | 332.12 ± 8.04 |
| Hybrid Algorithm | 152.22 ± 0.88 ★ | 247.55 ± 1.03 ★ | 347.40 ± 0.96 ★ |
| Kruskal-Wallis p | p < 0.001 *** | p < 0.001 *** | p < 0.001 *** |

รูปที่ 4.1 กราฟ Convergence ของ GA และ Hybrid Algorithm ทั้ง 3 Scenarios
ทดสอบ Backend API ด้วย budget 20,000 บาท ทริป 3 วัน 2 คน พบว่าระบบสร้าง 3 packages ได้ถูกต้อง โดย Budget package เลือก Rawai Beachfront Hostel (รวม 7,614 บาท), Standard package เลือก Novotel Karon (รวม 15,418 บาท), และ Premium package ที่เลือก Anantara Layan ระบบรายงานว่างบไม่พอ ทั้งหมดใช้เวลาประมวลผลรวมประมาณ 4 วินาที ส่วน Frontend พัฒนาเสร็จแล้วภายใต้ชื่อ WeEasyTrip ใช้ HTML + vanilla JavaScript + Leaflet.js มีระบบ dark/light theme, glass-morphism design, calendar date picker (รองรับการต่อยอด AI ค้นหาราคาห้องพักตามฤดูกาลในอนาคต), dropdown เลือกจังหวัด (เปิดเฉพาะภูเก็ตในระยะ PoC แต่ออกแบบให้ขยายได้), แสดงเส้นทางบนแผนที่แบบ multi-day มี custom marker หมายเลข ลำดับ-วัน polyline แยกสีแต่ละวัน และ panel รายละเอียดที่ผู้ใช้สามารถ swap จุด ลบจุด หรือเพิ่มจุดได้ผ่าน modal พร้อม category filter โดยระบบจะคำนวณเส้นทางและค่าใช้จ่ายใหม่ทันที (< 1 มิลลิวินาที) ผ่าน /api/recompute













# ทรัพยากรและแผนการดำเนินงาน

## การจัดเตรียมฮาร์ดแวร์และซอฟต์แวร์
ส่วนนี้ระบุทรัพยากรที่ใช้ในการพัฒนาและทดสอบระบบ
### ฮาร์ดแวร์
เครื่องคอมพิวเตอร์ส่วนบุคคลของผู้พัฒนา ที่ใช้ในการ implement และทดสอบ มีคุณสมบัติขั้นต่ำ CPU 4 cores, RAM 8 GB, SSD 256 GB ระบบไม่มีความต้องการ GPU หรือ server เฉพาะ เนื่องจากปัญหามีขนาดเล็กพอที่จะรันบนเครื่องส่วนบุคคลได้
### ซอฟต์แวร์และเครื่องมือ
Python 3.10+ ใช้ในการ implement Algorithm Engine และ Backend API ร่วมกับ library ได้แก่ FastAPI (สำหรับ REST API), Uvicorn (ASGI server), NumPy (สำหรับการคำนวณ vectorized), Pydantic (สำหรับ data validation)
Frontend ใช้ HTML5, CSS3, JavaScript (ES6) แบบ vanilla พร้อม Leaflet.js (สำหรับแผนที่) และ Chart.js (สำหรับ graph) ไม่ใช้ framework เพื่อให้ระบบเบาและ deploy ได้ง่าย
เครื่องมือสนับสนุนได้แก่ Visual Studio Code (IDE), Git (version control), GitHub (repository hosting), Postman (API testing), และ Microsoft Word (สำหรับเขียนรายงาน)
## แผนการดำเนินงาน
แผนการดำเนินงานของโครงงานแบ่งออกเป็น 2 ส่วน คือ
(1) งานที่ดำเนินการเสร็จแล้วในช่วงโครงงานพิเศษ 1
(2) งานที่จะดำเนินการต่อในโครงงานพิเศษ 2 รายละเอียดในตารางด้านล่าง
งานในช่วงโครงงานพิเศษ 1 ที่ดำเนินการเสร็จแล้วได้แก่ การกำหนดหัวข้อโครงงาน การทบทวนวรรณกรรมที่เกี่ยวข้อง การ formulate ปัญหาในเชิงคณิตศาสตร์ การจัดทำ dataset ภูเก็ต การ implement Greedy baseline และ Genetic Algorithm รุ่นแรก การพัฒนา Backend API การพัฒนา Frontend UI ส่วนต้น และการเขียนรายงานฉบับนี้
แนวทางการพัฒนาต่อในโครงงานพิเศษ 2 ได้แก่
(1) Multi-objective Optimization — ปัจจุบันระบบ optimize เฉพาะ score แต่ยังไม่ balance ระหว่าง score / ความหลากหลายของหมวดหมู่ / ระยะทางรวม สามารถพัฒนาเป็น Pareto front เพื่อให้ผู้ใช้เลือก trade-off ที่ต้องการได้
(2) Reinforcement Learning Agent — แทนที่ Greedy seed ด้วย RL agent ที่เรียนรู้จากประวัติการเลือก POI ของผู้ใช้เพื่อให้คำแนะนำที่ดีขึ้นเรื่อยๆ
(3) Real-time Re-optimization — เมื่อผู้ใช้ swap หรือลบ POI ระบบควร recompute ทั้ง package ใหม่ด้วย Hybrid Algorithm แทนที่จะคำนวณเฉพาะค่าใช้จ่าย
(4) Dynamic Pricing — ดึงราคาห้องพักจริงจาก Agoda หรือ Booking.com API แทน static dataset เพื่อให้งบประมาณแม่นยำขึ้น
(5) เวลาเปิด-ปิดจริง — ดึงข้อมูลจาก Google Places API แทน time window ที่ประมาณไว้
(6) Rating และรีวิว — นำ Google หรือ TripAdvisor rating มาเป็น weight ใน score function เพื่อเพิ่มคุณภาพของ POI ที่แนะนำ
(7) ขยายจังหวัด — จากภูเก็ตไปยังจังหวัดท่องเที่ยวอื่น เช่น เชียงใหม่ กระบี่ เกาะสมุย และจังหวัดอื่นทั้ง 77 จังหวัดตาม dropdown ที่ออกแบบไว้
(8) User Preference — ให้ผู้ใช้ระบุความชอบ/ข้อจำกัด (เช่น ไม่กินเนื้อ ชอบธรรมชาติ หลีกเลี่ยงสถานที่คนพลุกพล่าน) เพื่อ filter POI ก่อน optimize
(9) Collaborative Planning — สร้าง shared link ให้กลุ่มเพื่อนร่วมวางแผนทริปใน session เดียวกันได้แบบ real-time
(10) Export Itinerary — ส่งออกแผนการเดินทางเป็น PDF itinerary หรือเพิ่มเข้า Google Calendar โดยอัตโนมัติ




ตารางที่ 4.2 การดำเนินงานที่ผ่านมาจนถึงปัจจุบัน
| ขั้นตอน | ม.ค.66 | ม.ค.66 | ม.ค.66 | ม.ค.66 | ม.ค.66 | ม.ค.66 | ม.ค.66 | ก.พ.66 | ก.พ.66 | ก.พ.66 | ก.พ.66 | มี.ค.66 | มี.ค.66 | มี.ค.66 | มี.ค.66 | มี.ค.66 | เม.ย.66 | เม.ย.66 | เม.ย.66 | เม.ย.66 | เม.ย.66 | พ.ค.66 | พ.ค.66 | พ.ค.66 | พ.ค.66 | พ.ค.66 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ขั้นตอน | 1 | 1 | 2 | 2 | 3 | 3 | 4 | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 | 1 | 1 | 2 | 3 | 4 | 1 | 1 | 2 | 3 | 4 |
| 1.กำหนดหัวข้อโครงงาน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2.ทบทวนวรรณกรรม |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3. วิเคราะห์และออกแบบระบบ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4. พัฒนาระบบต้นแบบ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5. ทดสอบระบบและเก็บผล |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6. นำเสนอข้อเสนอโครงงาน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

ตารางที่ 4.3 แผนการดำเนินงานในอนาคต
| ขั้นตอน | ก.ค.69 | ก.ค.69 | ก.ค.69 | ก.ค.69 | ส.ค.69 | ส.ค.69 | ส.ค.69 | ส.ค.69 | ก.ย.69 | ก.ย.69 | ก.ย.69 | ก.ย.69 | ต.ค.69 | ต.ค.69 | ต.ค.69 | ต.ค.69 | พ.ย.69 | พ.ย.69 | พ.ย.69 | พ.ย.69 | พ.ย.69 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 |
| 1.แก้ไขโครงงานตาม ข้อเสนอแนะของ อาจารย์ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2.แก้ไขเว็บแอป พลิเคชัน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3.ทดสอบและแก้ไขเว็บ แอปพลิเคชัน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4.สรุปผลการทำโครงงาน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |




# สรุป
โครงงานนี้นำเสนอระบบสร้างและเพิ่มประสิทธิภาพเส้นทางการท่องเที่ยวภายใต้งบประมาณโดยใช้ปัญญาประดิษฐ์ โดยใช้จังหวัดภูเก็ตเป็น case study ใน Project 1 ระบบแก้ปัญหา Budget-Constrained Team Orienteering Problem with Time Windows ด้วยการเปรียบเทียบ 3 อัลกอริทึม ได้แก่ Greedy Algorithm (baseline), Genetic Algorithm, และ Hybrid Algorithm ที่นำเสนอใหม่ ฐานข้อมูล 164 จุดดึงจาก OpenStreetMap ครอบคลุม 7 หมวดหมู่ พร้อมโรงแรม 20 แห่ง ผลการทดลอง 135 trials (15 รอบ × 3 scenarios × 3 อัลกอริทึม) ยืนยันว่า Hybrid Algorithm ให้ score สูงสุดในทุก scenario (S1: 152.2, S2: 247.5, S3: 347.4) โดยมีนัยสำคัญทางสถิติ (Kruskal-Wallis p<0.001) พร้อม structured day pattern (attr-attr-lunch-attr-attr-dinner) ครบทุกวัน ด้วยเวลาประมวลผล 120-270 มิลลิวินาที ยืนยันความเหนือกว่าของแนวทาง Hybrid ในการแก้ปัญหา B-TOPTW
ในขั้นต่อไป (Project 2) โครงงานจะมุ่งพัฒนาใน 3 ด้านหลัก ได้แก่
(1) ด้าน Algorithm: Multi-objective Optimization ที่ balance ระหว่าง score / ความหลากหลาย / ระยะทาง, Reinforcement Learning Agent แทน Greedy seed, และ Real-time Re-optimization เมื่อผู้ใช้แก้ไขแผน
(2) ด้านข้อมูล: ราคา dynamic จาก Agoda/Booking.com API, เวลาเปิด-ปิดจาก Google Places API, rating จาก TripAdvisor เป็น score weight, และขยายครอบคลุมทั้ง 77 จังหวัดทั่วประเทศไทย
(3) ด้าน UX: ระบบ User Preference สำหรับ filter POI ตามความชอบ, Collaborative Planning ผ่าน shared link, และ Export เป็น PDF itinerary หรือ Google Calendar เพื่อนำไปสู่ระบบที่สมบูรณ์และพร้อมใช้งานจริงในระดับ production



รายการอ้างอิง
[1] Vansteenwegen, P., Souffriau, W., & Van Oudheusden, D. (2011). The Orienteering Problem: A Survey. European Journal of Operational Research, 209(1), 1-10.
[2] Gunawan, A., Lau, H. C., & Vansteenwegen, P. (2016). Orienteering Problem: A Survey of Recent Variants, Solution Approaches and Applications. European Journal of Operational Research, 255(2), 315-332.
[3] Gavalas, D., Konstantopoulos, C., Mastakas, K., & Pantziou, G. (2014). A Survey on Algorithmic Approaches for Solving Tourist Trip Design Problems. Journal of Heuristics, 20(3), 291-328.
[4] Souffriau, W., Vansteenwegen, P., Vanden Berghe, G., & Van Oudheusden, D. (2008). A Greedy Randomised Adaptive Search Procedure for the Team Orienteering Problem. Journal of Heuristics, 14(4), 327-346.
[5] Holland, J. H. (1992). Adaptation in Natural and Artificial Systems. MIT Press.
[6] Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization and Machine Learning. Addison-Wesley.
[7] Vansteenwegen, P., Souffriau, W., Vanden Berghe, G., & Van Oudheusden, D. (2009). Iterated Local Search for the Team Orienteering Problem with Time Windows. Computers & Operations Research, 36(12), 3281-3290.
[8] Lin, S., & Yu, V. F. (2012). A Simulated Annealing Heuristic for the Team Orienteering Problem with Time Windows. European Journal of Operational Research, 217(1), 94-107.




ภาคผนวก
ภาคผนวก ก ภาพหน้าจอระบบ WeEasyTrip
ภาคผนวกนี้แสดงภาพหน้าจอของระบบ WeEasyTrip ที่พัฒนาในโครงงานนี้ ครอบคลุมทุกขั้นตอนการใช้งานตั้งแต่กรอกข้อมูล จนถึงการปรับแต่งแพ็กเกจ
รูปที่ ก.1 หน้าหลักและฟอร์มกรอกข้อมูลของระบบ WeEasyTrip

รูปที่ ก.2 หน้าแสดงผล 3 แพ็กเกจ (Budget / Standard / Premium)



รูปที่ ก.3 หน้ารายละเอียดแพ็กเกจและแผนที่เส้นทาง

รูปที่ ก.4 หน้าต่างการเปลี่ยนสถานที่ (Swap Modal)


รูปที่ ก.5 กราฟ Convergence ของ GA และ Hybrid Algorithm ทั้ง 3 Scenarios

ภาคผนวก ข ผลการทดลองแบบละเอียดทุก Trial
ตารางต่อไปนี้แสดงคะแนนรวม (Total Score) ของแต่ละ Trial สำหรับ 3 อัลกอริทึม บน 3 Scenarios โดย Greedy Algorithm เป็น Deterministic (ไม่มี Randomness) จึงรันเพียง 1 ครั้ง ส่วน GA และ Hybrid รัน 15 ครั้งต่อ Scenario
ตาราง ข.1 ผลทุก Trial — Scenario 1 (3 วัน, งบ 10,000 บาท)
| Trial | Greedy Algorithm | Genetic Algorithm (GA) | Hybrid Algorithm |
| --- | --- | --- | --- |
| 1 | 148.1 | 150.6 | 153.0 |
| 2 | 148.1 | 148.6 | 151.6 |
| 3 | 148.1 | 146.6 | 153.1 |
| 4 | 148.1 | 148.0 | 152.8 |
| 5 | 148.1 | 145.4 | 151.9 |
| 6 | 148.1 | 147.6 | 152.5 |
| 7 | 148.1 | 150.4 | 152.6 |
| 8 | 148.1 | 149.9 | 152.2 |
| 9 | 148.1 | 140.3 | 151.8 |
| 10 | 148.1 | 145.5 | 151.9 |
| 11 | 148.1 | 151.1 | 152.4 |
| 12 | 148.1 | 148.9 | 151.6 |
| 13 | 148.1 | 141.7 | 154.0 |
| 14 | 148.1 | 147.2 | 151.8 |
| 15 | 148.1 | 150.8 | 150.1 |
| Mean ± Std | 148.10 ± 0.00 | 147.51 ± 3.23 | 152.22 ± 0.88 |
ตาราง ข.2 ผลทุก Trial — Scenario 2 (5 วัน, งบ 15,000 บาท)
| Trial | Greedy Algorithm | Genetic Algorithm (GA) | Hybrid Algorithm |
| --- | --- | --- | --- |
| 1 | 244.6 | 246.7 | 246.7 |
| 2 | 244.6 | 244.1 | 246.7 |
| 3 | 244.6 | 242.6 | 248.7 |
| 4 | 244.6 | 240.9 | 247.3 |
| 5 | 244.6 | 244.7 | 247.0 |
| 6 | 244.6 | 244.0 | 248.4 |
| 7 | 244.6 | 245.0 | 248.9 |
| 8 | 244.6 | 245.7 | 246.4 |
| 9 | 244.6 | 246.5 | 248.5 |
| 10 | 244.6 | 242.2 | 248.4 |
| 11 | 244.6 | 245.8 | 245.6 |
| 12 | 244.6 | 245.0 | 248.7 |
| 13 | 244.6 | 245.2 | 247.8 |
| 14 | 244.6 | 244.1 | 247.7 |
| 15 | 244.6 | 244.8 | 246.5 |
| Mean ± Std | 244.60 ± 0.00 | 244.49 ± 1.59 | 247.55 ± 1.03 |
ตาราง ข.3 ผลทุก Trial — Scenario 3 (7 วัน, งบ 25,000 บาท)
| Trial | Greedy Algorithm | Genetic Algorithm (GA) | Hybrid Algorithm |
| --- | --- | --- | --- |
| 1 | 346.7 | 332.8 | 346.9 |
| 2 | 346.7 | 333.9 | 348.0 |
| 3 | 346.7 | 332.6 | 347.8 |
| 4 | 346.7 | 334.9 | 347.1 |
| 5 | 346.7 | 338.1 | 348.5 |
| 6 | 346.7 | 333.6 | 346.2 |
| 7 | 346.7 | 334.3 | 345.8 |
| 8 | 346.7 | 303.6 | 348.2 |
| 9 | 346.7 | 334.0 | 348.4 |
| 10 | 346.7 | 335.3 | 347.8 |
| 11 | 346.7 | 334.6 | 347.3 |
| 12 | 346.7 | 334.7 | 345.9 |
| 13 | 346.7 | 331.2 | 348.3 |
| 14 | 346.7 | 335.0 | 348.4 |
| 15 | 346.7 | 333.2 | 346.4 |
| Mean ± Std | 346.70 ± 0.00 | 332.12 ± 8.04 | 347.40 ± 0.96 |

ภาคผนวก ค ตัวอย่างโครงสร้างข้อมูล POI และโรงแรม
ฐานข้อมูลสถานที่ท่องเที่ยวภูเก็ตจัดเก็บในรูปแบบ JSON ไฟล์ phuket_pois.json ประกอบด้วย 2 ส่วนหลัก คือ pois (164 รายการ) และ hotels (20 รายการ) โดยมีโครงสร้างฟิลด์ดังตารางต่อไปนี้
ตาราง ค.1 โครงสร้างฟิลด์ของข้อมูล POI
| ฟิลด์ | ประเภท | คำอธิบาย |
| --- | --- | --- |
| name_en | String | ชื่อสถานที่เป็นภาษาอังกฤษ |
| name_th | String | ชื่อสถานที่เป็นภาษาไทย |
| category | String | หมวดหมู่ (beach, temple, restaurant, viewpoint, market, culture, activity) |
| lat / lng | Float | พิกัดละติจูด / ลองจิจูด (WGS84) |
| score | Float | คะแนนความน่าสนใจ ช่วง 1.0–10.0 |
| cost | Integer | ค่าใช้จ่ายต่อคน (บาท) — 0 หมายถึงไม่มีค่าเข้า |
| duration_min | Integer | เวลาที่แนะนำในการเยี่ยมชม (นาที) |
| open_min | Integer | เวลาเปิด นับจากเที่ยงคืน (นาที) เช่น 360 = 06:00 |
| close_min | Integer | เวลาปิด นับจากเที่ยงคืน (นาที) เช่น 1320 = 22:00 |
| tags | Array | ป้ายกำกับสำหรับการค้นหาและกรองข้อมูล |
| id | String | รหัสเฉพาะ เช่น P01, P51 (POI) หรือ H01 (Hotel) |
ตาราง ค.2 ตัวอย่างข้อมูล POI จากฐานข้อมูล
| ชื่อสถานที่ | หมวดหมู่ | Score | Cost (฿/คน) | เวลาเปิด-ปิด |
| --- | --- | --- | --- | --- |
| Patong Beach | beach | 8.5 | 0 | 06:00–22:00 |
| Wat Chalong | temple | 8.2 | 0 | 07:00–17:00 |
| Kan Eang@Pier | restaurant | 8.5 | 400 | 11:00–22:00 |
| Big Buddha | culture | 9.0 | 0 | 06:00–19:30 |
| ATV Phuket | activity | 7.8 | 1200 | 09:00–17:00 |
| Rawai Seafood Market | market | 7.5 | 300 | 08:00–22:00 |
หมายเหตุ: open_min และ close_min คือจำนวนนาทีนับจากเที่ยงคืน เช่น open_min=360 หมายถึงเปิดเวลา 06:00 น. และ close_min=1320 หมายถึงปิดเวลา 22:00 น.
ตาราง ค.3 ตัวอย่างข้อมูลโรงแรมทั้ง 3 ระดับ
| ชื่อโรงแรม | ดาว | ราคา/คืน (฿) | Score | ระดับ |
| --- | --- | --- | --- | --- |
| Lub d Phuket Patong | 1 | 450 | 7.8 | Budget |
| Novotel Karon Beach | 4 | 3500 | 8.6 | Standard |
| Anantara Layan Phuket | 5 | 8000 | 9.4 | Premium |
โรงแรมแบ่งเป็น 3 tier ตามจำนวนดาวและราคา: Budget (1-2 ดาว ≤ 1,500 บาท/คืน), Standard (3-4 ดาว 1,500–5,000 บาท/คืน) และ Premium (4-5 ดาว > 5,000 บาท/คืน) โดย Backend จะเลือกโรงแรมที่เหมาะสมกับงบประมาณในแต่ละ tier อัตโนมัติ
