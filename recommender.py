
def generate_recomendatation(df):
    res=[]
    if df['usage_kwh'].mean() >0.1:
        res.append("consider using high-power devices")
    if df['usage_kwh'].max() >1:
        res.append("High voltage occured: check your devices")
    return res