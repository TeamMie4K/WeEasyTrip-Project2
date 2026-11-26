/**
 * สร้าง Google Form แบบสอบถามหลังทดสอบ WeEasyTrip (ข้อมูลผู้ทดสอบ + SUS 10 ข้อ + คำถามปลายเปิด)
 * พร้อม Google Sheet เก็บคำตอบ และแผ่น "คะแนน SUS" ที่คิดคะแนน 0-100 ให้อัตโนมัติทุกแถว
 *
 * วิธีใช้
 *  1) เปิด https://script.google.com แล้วกด "โครงการใหม่"
 *  2) ลบโค้ดเดิม วางโค้ดทั้งไฟล์นี้ แล้วกดบันทึก
 *  3) เลือกฟังก์ชัน createUsabilityForm แล้วกด "เรียกใช้" (ครั้งแรกต้องอนุญาตสิทธิ์ Forms/Sheets/Drive ของบัญชีตัวเอง)
 *  4) ดูลิงก์ฟอร์มและชีตที่หน้าต่าง "บันทึกการดำเนินการ" (Execution log) ส่งลิงก์ฟอร์มให้ผู้ทดสอบกรอกหลังทำภารกิจ
 *
 * ส่วนที่ผู้จัดทำบันทึกเอง (สำเร็จ/เวลา/กดผิดของภารกิจ T1-T6) ใช้ docs/usability_test_kit.docx ตามเดิม
 */
function createUsabilityForm() {
  var form = FormApp.create('แบบสอบถามหลังทดสอบเว็บ WeEasyTrip');
  form.setDescription('ขอบคุณที่ช่วยทดสอบ ไม่มีคำตอบถูกหรือผิด เรากำลังประเมินเว็บ ไม่ได้ประเมินตัวคุณ ใช้เวลาประมาณ 5 นาที คำตอบไม่ระบุชื่อ (ใช้รหัสผู้ทดสอบที่ผู้จัดทำให้)');
  form.setCollectEmail(false);
  form.setConfirmationMessage('ขอบคุณสำหรับการตอบแบบสอบถาม');

  // ---- ส่วนที่ 1: ข้อมูลผู้ทดสอบ ----
  form.addTextItem().setTitle('รหัสผู้ทดสอบ (เช่น P1, P2)').setRequired(true);
  form.addTextItem().setTitle('อายุ (ปี)').setRequired(false);
  form.addMultipleChoiceItem().setTitle('ประสบการณ์วางแผนเที่ยวด้วยเว็บหรือแอป')
      .setChoiceValues(['น้อย', 'ปานกลาง', 'มาก']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('อุปกรณ์ที่ใช้ทดสอบ')
      .setChoiceValues(['คอมพิวเตอร์', 'มือถือ']).setRequired(true);

  // ---- ส่วนที่ 2: SUS ----
  form.addPageBreakItem().setTitle('ส่วนที่ 2: ความคิดเห็นต่อการใช้งานเว็บ')
      .setHelpText('ให้คะแนน 1 = ไม่เห็นด้วยอย่างยิ่ง ถึง 5 = เห็นด้วยอย่างยิ่ง');
  var sus = [
    'ฉันคิดว่าฉันอยากใช้ระบบนี้บ่อย ๆ',
    'ฉันรู้สึกว่าระบบนี้ซับซ้อนโดยไม่จำเป็น',
    'ฉันคิดว่าระบบนี้ใช้งานง่าย',
    'ฉันคิดว่าฉันต้องมีผู้ช่วยทางเทคนิคจึงจะใช้ระบบนี้ได้',
    'ฉันพบว่าฟังก์ชันต่าง ๆ ของระบบนี้ทำงานรวมกันได้ดี',
    'ฉันคิดว่าระบบนี้มีความไม่สอดคล้องกันมากเกินไป',
    'ฉันคิดว่าคนส่วนใหญ่จะเรียนรู้การใช้ระบบนี้ได้อย่างรวดเร็ว',
    'ฉันพบว่าระบบนี้ใช้งานยุ่งยากมาก',
    'ฉันรู้สึกมั่นใจเมื่อใช้ระบบนี้',
    'ฉันต้องเรียนรู้หลายอย่างก่อนที่จะใช้ระบบนี้ได้'
  ];
  sus.forEach(function (q, i) {
    form.addScaleItem().setTitle((i + 1) + '. ' + q)
        .setBounds(1, 5).setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง').setRequired(true);
  });

  // ---- ส่วนที่ 3: คำถามปลายเปิด ----
  form.addPageBreakItem().setTitle('ส่วนที่ 3: ข้อเสนอแนะ');
  form.addParagraphTextItem().setTitle('ส่วนไหนของเว็บที่ใช้แล้วสับสนที่สุด');
  form.addParagraphTextItem().setTitle('แผนที่เว็บจัดให้ ดูสมเหตุสมผลและเที่ยวตามได้จริงไหม เพราะอะไร');
  form.addParagraphTextItem().setTitle('ถ้าแก้ได้ 1 อย่าง อยากให้แก้อะไร');

  // ---- ชีตเก็บคำตอบ + แผ่นคิดคะแนน SUS ----
  var ss = SpreadsheetApp.create('ผลแบบสอบถาม WeEasyTrip');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  SpreadsheetApp.flush();

  var resp = null;
  ss.getSheets().forEach(function (s) {
    if (!resp && /Form Responses|การตอบแบบฟอร์ม/i.test(s.getName())) resp = s;
  });
  if (resp) {
    // คอลัมน์ของชีตคำตอบ: A เวลา, B รหัส, C อายุ, D ประสบการณ์, E อุปกรณ์, F-O = SUS ข้อ 1-10
    var calc = ss.insertSheet('คะแนน SUS');
    var n = "'" + resp.getName() + "'!";
    calc.getRange('A1:C1').setValues([['รหัสผู้ทดสอบ', 'คะแนน SUS (0-100)', 'การแปลผล']]);
    calc.getRange('A2').setFormula('=ARRAYFORMULA(IF(' + n + 'B2:B="","",' + n + 'B2:B))');
    var f = '=ARRAYFORMULA(IF(' + n + 'F2:F="","",('
          + '(' + n + 'F2:F-1)+(5-' + n + 'G2:G)+(' + n + 'H2:H-1)+(5-' + n + 'I2:I)+(' + n + 'J2:J-1)'
          + '+(5-' + n + 'K2:K)+(' + n + 'L2:L-1)+(5-' + n + 'M2:M)+(' + n + 'N2:N-1)+(5-' + n + 'O2:O))*2.5))';
    calc.getRange('B2').setFormula(f);
    calc.getRange('C2').setFormula('=ARRAYFORMULA(IF(B2:B="","",IF(B2:B>=80,"ดีมาก",IF(B2:B>=68,"ดีกว่าค่าเฉลี่ย",IF(B2:B>=51,"ปานกลาง","ควรปรับปรุง")))))');
    calc.getRange('E1').setValue('ค่าเฉลี่ย SUS ทั้งกลุ่ม');
    calc.getRange('E2').setFormula('=IFERROR(AVERAGE(B2:B),"")');
    calc.getRange('E4').setValue('จำนวนผู้ตอบ');
    calc.getRange('E5').setFormula('=COUNT(B2:B)');
    calc.getRange('A1:E1').setFontWeight('bold');
  } else {
    Logger.log('ยังไม่พบชีตคำตอบ: ให้เปิดฟอร์มกดส่งคำตอบทดสอบ 1 ครั้งก่อน แล้วรันฟังก์ชันนี้ใหม่ หรือสร้างแผ่นคิดคะแนนเองตามสูตร SUS');
  }

  Logger.log('ลิงก์ให้ผู้ทดสอบกรอก: ' + form.getPublishedUrl());
  Logger.log('ลิงก์แก้ไขฟอร์ม: ' + form.getEditUrl());
  Logger.log('ชีตผลลัพธ์: ' + ss.getUrl());
}
