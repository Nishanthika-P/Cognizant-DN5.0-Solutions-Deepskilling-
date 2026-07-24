"""
seed_data.py
Hands-On 5, Task 1, step 51: insert sample rows via the ORM.
Run with:  flask shell < ../seed_data.py
(from inside the flask_coursemanager/ directory, with FLASK_APP=app.py)
"""
from app import db
from courses.models import Department, Course

cs = Department(name='Computer Science', head_of_dept='Dr. Rao', budget=500000)
ee = Department(name='Electronics', head_of_dept='Dr. Iyer', budget=350000)
db.session.add_all([cs, ee])
db.session.commit()

c1 = Course(name='Data Structures', code='CS101', credits=4, department=cs)
c2 = Course(name='Operating Systems', code='CS102', credits=4, department=cs)
c3 = Course(name='Digital Circuits', code='EE101', credits=3, department=ee)
db.session.add_all([c1, c2, c3])
db.session.commit()

print('Seeded:', Course.query.all())
