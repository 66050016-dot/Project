import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import plotly.express as px

def analyze_health_factors(df: pd.DataFrame):
    # ใช้ข้อมูลจริง: ดูว่าปัจจัยไหนทำให้คนเผาผลาญแคลอรี่ (Calories_Burned) ได้มากที่สุด
    features = ['Age', 'Weight (kg)', 'Session_Duration (hours)', 'Water_Intake (liters)', 'Workout_Frequency (days/week)', 'Max_BPM']
    
    # ทำความสะอาดข้อมูลเบื้องต้น
    df_clean = df.dropna(subset=features + ['Calories_Burned'])
    
    X = df_clean[features]
    y = df_clean['Calories_Burned']
    
    # แบ่งข้อมูลสอน AI (Train) 80% และทดสอบ (Test) 20%
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # ฝึกโมเดล Regression (ทำนายตัวเลขแคลอรี่)
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    
    # ประเมินผลความแม่นยำ (R-Squared)
    r2 = r2_score(y_test, y_pred)
    
    # ดึงค่าอิทธิพลของแต่ละปัจจัย
    importance_df = pd.DataFrame({
        'ปัจจัย (Features)': ['อายุ', 'น้ำหนัก (กก.)', 'เวลาออกกำลังกาย (ชม.)', 'ดื่มน้ำ (ลิตร)', 'ความถี่ (วัน/สัปดาห์)', 'อัตราเต้นหัวใจสูงสุด'],
        'อิทธิพลต่อการเผาผลาญ (%)': (rf.feature_importances_ * 100).round(2)
    }).sort_values('อิทธิพลต่อการเผาผลาญ (%)', ascending=True)
    
    # สร้างกราฟ Plotly
    fig = px.bar(importance_df, x='อิทธิพลต่อการเผาผลาญ (%)', y='ปัจจัย (Features)', 
                 orientation='h', title='📊 ปัจจัยใดส่งผลต่อการเผาผลาญพลังงาน (Calories Burned) มากที่สุด?',
                 color='อิทธิพลต่อการเผาผลาญ (%)', color_continuous_scale='Sunset')
    
    return r2, fig