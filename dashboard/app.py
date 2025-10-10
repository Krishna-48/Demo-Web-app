
import streamlit as st
import pandas as pd
import requests
from components import styled_status

API_BASE = st.secrets.get('API_BASE', 'http://127.0.0.1:8000')

st.set_page_config(page_title='DR Exercise Dashboard', layout='wide')
st.title('🌩️ Disaster Recovery Exercise Management (Demo)')

col1, col2 = st.columns([2,1])

with col2:
    if st.button('🔁 Refresh DR Data (backend)'):
        try:
            requests.post(f'{API_BASE}/api/devices/refresh', timeout=5)
        except Exception as e:
            st.error('Could not call backend: ' + str(e))

with col1:
    st.markdown('### Overview')
    try:
        r = requests.get(f'{API_BASE}/api/reports/summary', timeout=5)
        if r.status_code==200:
            summary = r.json()
            st.metric('Total Components', summary['count'], delta=None)
            st.metric('Average Recovery %', f"{summary['avg_recovery']}%", delta=None)
            st.json(summary['status_counts'])
    except Exception as e:
        st.warning('Backend not available: ' + str(e))

st.markdown('---')
st.markdown('### Components / Devices')
try:
    r = requests.get(f'{API_BASE}/api/devices', timeout=5)
    data = r.json() if r.status_code==200 else []
    df = pd.DataFrame(data)
    if not df.empty:
        df_display = df[['id','name','type','status','recovery_percent','last_checked']]
        st.dataframe(df_display)
        st.bar_chart(df.set_index('name')['recovery_percent'])
        # show card style
        st.markdown('### Detailed Cards')
        for _, row in df.iterrows():
            st.markdown(f"**{row['name']}** — {row['type']} — {styled_status(row['status'])}")
            st.progress(int(row['recovery_percent'] or 0))
            st.write(row.get('details',''))
    else:
        st.info('No devices. Click Refresh DR Data.')
except Exception as e:
    st.error('Error fetching devices: ' + str(e))

st.markdown('---')
st.markdown('### Upload / View Documents')
uploaded = st.file_uploader('Upload document (SOP / Guide)', type=['pdf','txt','md'])
if uploaded is not None:
    files = {'file': (uploaded.name, uploaded.getvalue())}
    try:
        resp = requests.post(f'{API_BASE}/api/upload', files=files)
        if resp.status_code==200:
            st.success('Uploaded: ' + resp.json().get('filename',''))
    except Exception as e:
        st.error('Upload failed: ' + str(e))

# List uploaded files
st.markdown('#### Uploaded files')
try:
    import os
    up_dir = 'backend/uploads'
    if os.path.exists(up_dir):
        files = os.listdir(up_dir)
        for f in files:
            st.write(f)
    else:
        st.write('No uploads yet.')
except Exception as e:
    st.write('Could not list uploads: '+str(e))
