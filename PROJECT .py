# # מנחש את שיטת הלמידה (ניסיונית או סטנדרטית)
# ### מגישים: תומר שביט ותמיר קינן
# ### תאריך הגשה: 1.6.2021

# ### מטרת המחקר היא למצוא על פי הנתונים מהי שיטת הלימוד שהתלמיד לומד (ניסיונית או סטנדרטית)?
# ### שאלת המחקר: כיצד הנתונים משפיעים על שיטת הלימוד?
# ### הנתונים - כל המשתנים מלבד משתנה המטרה (שיטת הלימוד)

# #### teaching_method -  שיטת לימוד, סטנדרטית או ניסיונית 
# #### school_type -   סוג בית הספר, פרטי או ציבורי
# #### n_student - מספר תלמידים בכיתה
# #### gender -  מין, זכר או נקבה
# #### lunch - האם התלמיד אוכל ארוחת צהריים או לא
# #### pretest - ציון התלמיד לפני הבחינה
# #### posttest - ציון לאחר הבחינה

# ## טעינת המידע

# #### ייבוא הספרייה

import pandas as pd

# #### טעינת המידע והדפסתו

df = pd.read_csv(r'C:\Users\Tamir\Documents\test_scores.csv')
print(df)

# #### הגדרת משתנה המטרה והנתונים  
# ##### המשתנה (המטרה) הוא בדיד, ישנן שתי אופציות של שיטת הלימוד   

x = df.drop(columns=['teaching_method'])
y = df['teaching_method']

# ## פיצול הנתונים

# #### ייבוא הספריה 

from sklearn.model_selection import train_test_split

# #### חלוקת המידע ביחס של 80/20

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# ## בניית המודלים של הסיווג

# #### יבוא המודלים

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
# #### הגדרת מסווגי הלמידה

names = ["Nearest_Neighbors", "Linear_SVM", "Polynomial_SVM", "RBF_SVM", "Gaussian_Process",
         "Decision_Tree", "Random_Forest", "AdaBoost",
         "Naive_Bayes", "SGD"]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(kernel="poly", degree=3, C=0.025),
    SVC(kernel="rbf", C=1, gamma=2),
    GradientBoostingClassifier(n_estimators=100, learning_rate=1.0),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=100),
    AdaBoostClassifier(n_estimators=100),
    GaussianNB(),
    SGDClassifier(loss="hinge", penalty="l2")]

# #### בתוך לולאה נעשית בניית המודל, החלת המודל על נתוני הבדיקה, חישוב ציון הדיוק של המודל ומציאת המודל עם הציון הגבוה ביותר 

scores = []
max_score = 0
for name, clf in zip(names, classifiers):
    clf.fit(x_train, y_train)
    score = clf.score(x_test, y_test)
    scores.append(score)
    if (max_score<score):
        max_score = score
        max_name = name
        max_clf = clf
        y_max_test = y_test
        y_pred = clf.predict(x_test)
print(scores)

# ## ניתוח ביצועי המודלים

# #### ייבוא הספרייה

import seaborn as sns

# ####  הכנסת נתוני הביצועים לטבלה עם צבעים והדפסתה 

gf = pd.DataFrame()
gf['name'] = names
gf['score'] = scores
cm = sns.light_palette("green", as_cmap=True)
s = gf.style.background_gradient(cmap=cm)
print(s)

# ####  חלוקה לעמודות לפי צבע והדפסתן

sns.set(style="whitegrid")
ax = sns.barplot(y="name", x="score", data=gf)

# #### הודעת פלט של המודל הטוב ביותר וציונו

print(max_name,"is the classifier with the highest score which is",max_score)

# ## שימוש במודל הטוב ביותר

# #### הכנסת נתוני הניבוא של המודל והתוצאות האמיתיות לטבלה והדפסת הטבלה

vs = pd.DataFrame()
vs['y_test'] = y_max_test
vs['y_pred'] = y_pred
print(vs)

# #### לולאה של קליטה מהמשתמש של הנתונים והדפסת החיזוי של הנתונים

max_clf.fit(x_train, y_train)
for num in range(2):
    public = float(input("enter the type of school either public(1) or non-public(0) "))
    number = float(input("enter the number of students in the class "))
    gender = float(input("enter the gender of the students: male(1) or female(0) "))
    lunch = float(input("enter whether a student qualifies for free/subsidized lunch(1) or not(0) "))
    pretest = float(input("enter the pretest score of the students out of 100 "))
    posttest = float(input("enter the posttest scores of the students out of 100 "))
    print(max_clf.predict([[public, number, gender, lunch, pretest, posttest]]))

# #### חיזוי של נתונים לא מהטבלה

print(max_clf.predict([[1, 24, 1, 1, 90, 100]]))

####  הדפסת חשיבות הנתונים

print(max_clf.feature_importances_)

from tkinter import *
from tkinter import messagebox
import tkinter as tk

top = Tk()

top.title('MODEL SELECTION')

top.geometry("1900x1500")

def a():
    clf = KNeighborsClassifier(3)
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def b():
    clf =     SVC(kernel="linear", C=0.025)
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def c():
    clf =     SVC(kernel="poly", degree=3, C=0.025)
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def d():
    clf =     SVC(kernel="rbf", C=1, gamma=2)
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def e():
    clf =    GradientBoostingClassifier(n_estimators=100, learning_rate=1.0)
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def f():
    clf =     DecisionTreeClassifier(max_depth=5)
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def g():
    clf =     RandomForestClassifier(max_depth=5, n_estimators=100)
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def h():
    clf =     AdaBoostClassifier(n_estimators=100)
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def i():
    clf =     GaussianNB()
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

def j():
    clf =     SGDClassifier(loss="hinge", penalty="l2")
    clf.fit(x_train, y_train)
    pred = [e1.get(), e2.get(),  e3.get(), e4.get(), e5.get(), e6.get()]
    pred = [int(i) for i in pred]
    per = clf.predict([pred])
    ans = "the teaching method is ", per
    tk.messagebox.showinfo("per", ans)

b1 = Button(top,text = "Nearest_Neighbors",activeforeground = "white",command=a ,activebackground = "black",width = 15, height = 3)
b2 = Button(top, text = "Linear_SVM",activeforeground = "white",command=b,activebackground = "black",width = 15, height = 3)  
b3 = Button(top, text = "Polynomial_SVM",activeforeground = "white",command=c,activebackground = "black",width = 15, height = 3)  
b4 = Button(top, text = "RBF_SVM",activeforeground = "white",command=d,activebackground = "black",width = 15, height = 3)  
b5 = Button(top,text = "Gaussian_Process",activeforeground = "white",command=e,activebackground = "black",width = 15, height = 3)  
b6 = Button(top, text = "Decision_Tree",activeforeground = "white",command=f,activebackground = "black",width = 15, height = 3)  
b7 = Button(top, text = "Random_Forest",activeforeground = "white",command=g,activebackground = "black",width = 15, height = 3)  
b8 = Button(top, text = "AdaBoost",activeforeground = "white",command=h,activebackground = "black",width = 15, height = 3)  
b9 = Button(top, text = "Naive_Bayes",activeforeground = "white",command=i,activebackground = "black",width = 15, height = 3)  
b10 = Button(top, text = "SGD",activeforeground = "white",command=j,activebackground = "black",width = 15, height = 3)  
exitButton = Button(top, text="Exit", command=top.destroy, activeforeground = "white",activebackground = "black",width = 15, height = 3)

Label(top, text="enter the type of school either public(1) or non-public(0) ").pack()
e1 = tk.Entry(top)
e1.pack()
Label(top, text="enter the number of students in the class ").pack()
e2 = tk.Entry(top)
e2.pack()
Label(top, text="enter the gender of the students: male(1) or female(0) ").pack()
e3 = tk.Entry(top)
e3.pack()
Label(top, text="enter whether a student qualifies for free/subsidized lunch(1) or not(0) ").pack()
e4 = tk.Entry(top)
e4.pack()
Label(top, text="enter the pretest score of the students out of 100 ").pack()
e5 = tk.Entry(top)
e5.pack()
Label(top, text="enter the posttest scores of the students out of 100 ").pack()
e6 = tk.Entry(top)
e6.pack()
Label(top, text="Standard(0) and Experimental(1)").pack()

def clickExitButton(top):
        exit()

b1.pack(side = RIGHT)
b2.pack(side = RIGHT)
b3.pack(side = RIGHT)
b4.pack(side = RIGHT)
b5.pack(side = RIGHT)
b6.pack(side = RIGHT)
b7.pack(side = RIGHT)
b8.pack(side = RIGHT)
b9.pack(side = RIGHT)
b10.pack(side = RIGHT)
exitButton.pack(side = LEFT)
top.mainloop()

# סיכום
#### school_type - משתנה בעל חשיבות נמוכה
#### n_student - משתנה בעל חשיבות גבוהה
#### gender - המשתנה בעל החשיבות הנמוכה ביותר
#### lunch - משתנה בעל חשיבות נמוכה
#### pretest - משתנה בעל חשיבות גבוהה
#### posttest - משתנה בעל חשיבות גבוהה
#### למידת מכונה היא תת-תחום במדעי המחשב ובבינה מלאכותית המשיק לתחומי הסטטיסטיקה והאופטימיזציה.
#### בתחום זה המחשב הוא הלומד.
#### אלגוריתמים של למידת מכונה משתמשים בשיטות חישוביות מתקדמות כדי “ללמוד” מידע ישירות מהנתונים ללא הסתמכות על משוואה קבועה מראש כמודל, הם פועלים במגוון משימות חישוביות בהן התכנות הקלאסי אינו אפשרי.
#### האלגוריתמים משתפרים באופן מיטבי בביצועיהם כאשר מספר הדגימות העומדות ללמידה גדל.
#### טכניקת ניתוח הנתונים מלמדת את המחשבים לעשות מה שבא באופן טבעי לבני אדם – ללמוד מניסיון.
#### שימוש בלמידת מכונה בא לידי ביטוי במיוחד כאשר יש צורך לחזות תרחישים מסוימים, או צורך לזהות דפוס התנהגותי מסוים, וכל זה מאוסף נתונים שקיים בארגון.
#### התהליכים דומים לאלה של כריית נתונים ומודלים לחיזוי.
### ?מה הבנתי על למידת מכונה
#### הבנו כי למידת מכונה היא ניתוח נתונים על ידי המחשב, בעזרת ספריות(אלגוריתמים) שונות המחשב לומד את הנתונים לבדו וככל שנותנים לו יותר "חומר"(נתונים) ללמוד כך הוא משתפר, השימוש בלמידת מכונה הוא למען חיזוי דברים או זיהוי שלהם מהנתונים. בנוסף הבנו כי למידת מכונה נחוצה בתחום ניתוח נתונים בפרט ובתחום התכנות בכלל. בעזרת למידת מכונה נוכל לנתח נתונים מכל סוג עבור בעיה מסויימת שלא ניתנת לפתירה על ידי כתיבת תוכנת מחשב.
### ?כיצד אפשר להשתמש בפרויקט
#### בעזרת פרויקט זה ניתן יהיה לבדוק על פי נתוני תלמיד פשוטים (מין, כמות תלמידים בכיתה, ציון לפני מבחן ועוד) את סוג הלימוד אותו הוא לומד, האם הוא לומד בשיטת לימוד ניסיונית, שיטת לימוד אחרת, שיטה שנמצאת בסוג של בדיקה, אם היא תצליח ותנפיק הישגים ישנה האופציה כי תהפוך לשיטה סטנדרטית שהיא כמובן שיטת הלימוד השנייה אשר כבר נחשבת מצליחה ומקובלת ברוב מוסדות החינוך. דרך הפרויקט לדוגמא נוכל ליצור מערכת שתזהה את שיטת הלימוד של הבית ספר לפי התלמידים שבו.