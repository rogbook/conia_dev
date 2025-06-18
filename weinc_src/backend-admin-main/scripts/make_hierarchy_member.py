import json

from sqlalchemy.orm import Session

from app.database.schema import Commission, Member, MemberClass, MemberMember, MemberCompany, SettingValue
from scripts.database.conn import db


def make_member_data(sess: Session, member: Member):
    mc = MemberClass.get(sess, member_id=member.id)
    cpn = MemberCompany.get(sess, member_id=member.id)
    cm = Commission.get(sess, target=member.id, default='Y')

    result = {
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "reg_date": member.reg_date,
        "class": mc.class_code if mc else None,
        "company_name": cpn.name if cpn else '',
        "commission": cm.value if cm else '',
        "sub": []
    }
    return result


def make_next_member(sess: Session, users):
    for user in users:
        sub_partners = sess.query(Member).join(MemberMember, MemberMember.member_id == Member.id).filter(MemberMember.pid == user['id']).all()

        for sub_partner in sub_partners:
            user['sub'].append(make_member_data(sess, sub_partner))
        make_next_member(sess, user['sub'])



if __name__ == '__main__':

    db.startup()

    session: Session
    with db.session as session:
        partners = session.query(Member).join(MemberClass, MemberClass.member_id == Member.id).filter(MemberClass.class_code != 'CM', MemberClass.class_code != None).all()

        top_users = []
        for partner in partners:
            top_user = session.query(MemberMember).filter(MemberMember.member_id == partner.id).all()
            if not top_user:
                top_users.append(make_member_data(session, partner))

        make_next_member(session, top_users)
        result_data = json.dumps(top_users, default=str)

        sv = SettingValue.get(session, type='member_hierarchy')
        sv.value = result_data
        session.commit()

    db.shutdown()
