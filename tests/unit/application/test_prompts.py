from aikos.application.prompts import female_thai


def test_male_forms_become_female():
    assert female_thai("สวัสดีครับ/ค่ะ ผมชื่อ ไอโกะ ครับ") == "สวัสดีค่ะ ฉันชื่อ ไอโกะ ค่ะ"
    assert female_thai("บอกเพิ่มได้ไหมครับ?") == "บอกเพิ่มได้ไหมคะ?"
    assert female_thai("ผมเป็นเลขา ผมคือไอโกะ") == "ฉันเป็นเลขา ฉันคือไอโกะ"


def test_leaves_other_text_alone():
    assert female_thai("ตัดผมพรุ่งนี้ 10 โมงค่ะ") == "ตัดผมพรุ่งนี้ 10 โมงค่ะ"  # ผม = hair
    assert female_thai("Hello, I'm Aiko.") == "Hello, I'm Aiko."
