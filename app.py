import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="🐉 Dragon Dash - Sweepstakes Dashboard",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4ECDC4;
    }
    .status-verified {
        color: #28a745;
        font-weight: bold;
    }
    .status-unverified {
        color: #dc3545;
        font-weight: bold;
    }
    .payout-confirmed {
        color: #28a745;
        font-weight: bold;
    }
    .payout-pending {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Main Header ----------
st.markdown("""
<div class="main-header">
    <h1>🐉 Dragon Dash Sweepstakes Dashboard</h1>
    <p>Complete Account Management & Transaction Tracking System</p>
</div>
""", unsafe_allow_html=True)

# ---------- Generate Demo Data ----------
@st.cache_data
def generate_demo_clients(num_clients=20):
    """Generate realistic demo client data"""
    first_names = [
        "Alexander", "Samantha", "Michael", "Jennifer", "Christopher", "Ashley", 
        "Matthew", "Jessica", "Andrew", "Sarah", "Joshua", "Amanda", "Daniel", 
        "Melissa", "David", "Nicole", "James", "Elizabeth", "Robert", "Stephanie"
    ]
    
    last_names = [
        "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", 
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", 
        "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee"
    ]
    
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com"]
    
    data = []
    random.seed(42)  # For consistent demo data
    
    for i in range(num_clients):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # Generate realistic transaction amounts
        cash_app = round(random.uniform(0, 1000), 2) if random.random() > 0.3 else 0
        zelle = round(random.uniform(0, 800), 2) if random.random() > 0.4 else 0
        paypal = round(random.uniform(0, 1200), 2) if random.random() > 0.2 else 0
        bank_transfer = round(random.uniform(0, 2000), 2) if random.random() > 0.6 else 0
        
        total_sent = cash_app + zelle + paypal + bank_transfer
        max_balance = round(random.uniform(500, 5000), 2)
        current_balance = round(max_balance - total_sent + random.uniform(-200, 500), 2)
        
        # Generate account status
        verified = random.choice([True, False])
        payout_status = random.choice(["Confirmed", "Pending", "Processing"])
        
        data.append({
            "Client ID": f"DD-{1000 + i:04d}",
            "Name": f"{first_name} {last_name}",
            "Email": f"{first_name.lower()}.{last_name.lower()}{random.randint(1,99)}@{random.choice(domains)}",
            "Verified": "✅ Verified" if verified else "❌ Unverified",
            "Max Balance": max_balance,
            "Current Balance": max(current_balance, 0),
            "Cash App Sent": cash_app,
            "Zelle Sent": zelle,
            "PayPal Sent": paypal,
            "Bank Transfer": bank_transfer,
            "Total Sent": total_sent,
            "Payout Status": payout_status,
            "Last Activity": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
            "Join Date": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        })
    
    return pd.DataFrame(data)

@st.cache_data
def generate_daily_logs(num_days=30):
    """Generate daily transaction logs"""
    logs = []
    total_cumulative = 0
    
    for day in range(num_days):
        date = (datetime.now() - timedelta(days=num_days - day - 1)).strftime("%Y-%m-%d")
        
        # Generate realistic daily amounts
        cash_app_daily = round(random.uniform(200, 1500), 2)
        zelle_daily = round(random.uniform(150, 1200), 2)
        paypal_daily = round(random.uniform(300, 2000), 2)
        bank_daily = round(random.uniform(100, 800), 2)
        
        daily_total = cash_app_daily + zelle_daily + paypal_daily + bank_daily
        total_cumulative += daily_total
        
        logs.append({
            "Date": date,
            "Cash App": cash_app_daily,
            "Zelle": zelle_daily,
            "PayPal": paypal_daily,
            "Bank Transfer": bank_daily,
            "Daily Total": daily_total,
            "Cumulative Total": total_cumulative,
            "Transactions": random.randint(5, 25)
        })
    
    return pd.DataFrame(logs)

@st.cache_data
def generate_payout_confirmations():
    """Generate payout confirmation data"""
    confirmations = []
    
    for i in range(15):
        confirmation_id = f"PAY-{random.randint(10000, 99999)}"
        amount = round(random.uniform(50, 2000), 2)
        method = random.choice(["Cash App", "Zelle", "PayPal", "Bank Transfer"])
        status = random.choice(["Completed", "Processing", "Failed"])
        
        confirmations.append({
            "Confirmation ID": confirmation_id,
            "Amount": amount,
            "Method": method,
            "Status": status,
            "Date": (datetime.now() - timedelta(days=random.randint(0, 14))).strftime("%Y-%m-%d %H:%M"),
            "Client ID": f"DD-{random.randint(1000, 1019):04d}"
        })
    
    return pd.DataFrame(confirmations)

# ---------- Load Data ----------
if 'client_data' not in st.session_state:
    st.session_state.client_data = generate_demo_clients()
if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = generate_daily_logs()
if 'payout_confirmations' not in st.session_state:
    st.session_state.payout_confirmations = generate_payout_confirmations()

client_df = st.session_state.client_data
logs_df = st.session_state.daily_logs
payouts_df = st.session_state.payout_confirmations

# ---------- Sidebar Filters ----------
st.sidebar.title("🔍 Dashboard Filters")

# Client filters
st.sidebar.subheader("Client Filters")
verification_filter = st.sidebar.selectbox(
    "Verification Status",
    ["All", "✅ Verified", "❌ Unverified"],
    key="verification_filter"
)

payout_filter = st.sidebar.selectbox(
    "Payout Status",
    ["All", "Confirmed", "Pending", "Processing"],
    key="payout_filter"
)

balance_range = st.sidebar.slider(
    "Current Balance Range",
    min_value=0,
    max_value=int(client_df["Current Balance"].max()),
    value=(0, int(client_df["Current Balance"].max())),
    step=100
)

# Date filter for logs
st.sidebar.subheader("Date Range")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime.now() - timedelta(days=7), datetime.now()),
    max_value=datetime.now()
)

# Apply filters
filtered_df = client_df.copy()

if verification_filter != "All":
    filtered_df = filtered_df[filtered_df["Verified"] == verification_filter]

if payout_filter != "All":
    filtered_df = filtered_df[filtered_df["Payout Status"] == payout_filter]

filtered_df = filtered_df[
    (filtered_df["Current Balance"] >= balance_range[0]) &
    (filtered_df["Current Balance"] <= balance_range[1])
]

# ---------- Main Dashboard ----------

# Key Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "👥 Total Clients",
        len(filtered_df),
        delta=f"{len(filtered_df) - len(client_df) + len(filtered_df)} filtered"
    )

with col2:
    total_sent = filtered_df["Total Sent"].sum()
    st.metric(
        "💸 Total Sent",
        f"${total_sent:,.2f}",
        delta=f"${total_sent/len(filtered_df):,.2f} avg" if len(filtered_df) > 0 else "N/A"
    )

with col3:
    total_balance = filtered_df["Current Balance"].sum()
    st.metric(
        "💰 Total Balance",
        f"${total_balance:,.2f}",
        delta=f"${total_balance/len(filtered_df):,.2f} avg" if len(filtered_df) > 0 else "N/A"
    )

with col4:
    verified_count = len(filtered_df[filtered_df["Verified"] == "✅ Verified"])
    verification_rate = (verified_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric(
        "✅ Verified Rate",
        f"{verification_rate:.1f}%",
        delta=f"{verified_count}/{len(filtered_df)}"
    )

with col5:
    confirmed_payouts = len(payouts_df[payouts_df["Status"] == "Completed"])
    st.metric(
        "✅ Confirmed Payouts",
        confirmed_payouts,
        delta=f"{len(payouts_df)} total"
    )

st.markdown("---")

# ---------- Client Accounts Table ----------
st.subheader("📋 Client Account Overview")

# Add search functionality
search_term = st.text_input("🔍 Search clients by name or email:", placeholder="Enter name or email...")

if search_term:
    filtered_df = filtered_df[
        filtered_df["Name"].str.contains(search_term, case=False, na=False) |
        filtered_df["Email"].str.contains(search_term, case=False, na=False)
    ]

# Format the dataframe for better display
display_df = filtered_df.copy()
display_df["Max Balance"] = display_df["Max Balance"].apply(lambda x: f"${x:,.2f}")
display_df["Current Balance"] = display_df["Current Balance"].apply(lambda x: f"${x:,.2f}")
display_df["Cash App Sent"] = display_df["Cash App Sent"].apply(lambda x: f"${x:,.2f}")
display_df["Zelle Sent"] = display_df["Zelle Sent"].apply(lambda x: f"${x:,.2f}")
display_df["PayPal Sent"] = display_df["PayPal Sent"].apply(lambda x: f"${x:,.2f}")
display_df["Bank Transfer"] = display_df["Bank Transfer"].apply(lambda x: f"${x:,.2f}")
display_df["Total Sent"] = display_df["Total Sent"].apply(lambda x: f"${x:,.2f}")

st.dataframe(
    display_df,
    use_container_width=True,
    height=400,
    column_config={
        "Client ID": st.column_config.TextColumn("Client ID", width="small"),
        "Name": st.column_config.TextColumn("Name", width="medium"),
        "Email": st.column_config.TextColumn("Email", width="large"),
        "Verified": st.column_config.TextColumn("Verified", width="small"),
        "Payout Status": st.column_config.TextColumn("Status", width="small"),
    }
)

# Export functionality
if st.button("📥 Export Client Data"):
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"dragon_dash_clients_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

st.markdown("---")

# ---------- Daily Transaction Logs ----------
st.subheader("📊 Daily Transaction Analytics")

# Filter logs by date range
if len(date_range) == 2:
    start_date, end_date = date_range
    logs_filtered = logs_df[
        (pd.to_datetime(logs_df["Date"]) >= pd.to_datetime(start_date)) &
        (pd.to_datetime(logs_df["Date"]) <= pd.to_datetime(end_date))
    ]
else:
    logs_filtered = logs_df

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["📈 Trends", "📋 Daily Logs", "💳 Payment Methods"])

with tab1:
    # Transaction trends chart
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Transaction Amounts', 'Cumulative Totals'),
        vertical_spacing=0.1
    )
    
    # Daily amounts
    fig.add_trace(
        go.Scatter(x=logs_filtered["Date"], y=logs_filtered["Daily Total"],
                  mode='lines+markers', name='Daily Total', line=dict(color='#4ECDC4')),
        row=1, col=1
    )
    
    # Cumulative totals
    fig.add_trace(
        go.Scatter(x=logs_filtered["Date"], y=logs_filtered["Cumulative Total"],
                  mode='lines', name='Cumulative Total', line=dict(color='#FF6B6B')),
        row=2, col=1
    )
    
    fig.update_layout(height=600, showlegend=True)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Amount ($)", row=1, col=1)
    fig.update_yaxes(title_text="Cumulative Amount ($)", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Daily logs table
    logs_display = logs_filtered.copy()
    for col in ["Cash App", "Zelle", "PayPal", "Bank Transfer", "Daily Total", "Cumulative Total"]:
        logs_display[col] = logs_display[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(logs_display, use_container_width=True, height=400)
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Days Tracked", len(logs_filtered))
    with col2:
        avg_daily = logs_filtered["Daily Total"].mean()
        st.metric("📊 Avg Daily", f"${avg_daily:,.2f}")
    with col3:
        total_period = logs_filtered["Daily Total"].sum()
        st.metric("💰 Period Total", f"${total_period:,.2f}")

with tab3:
    # Payment method breakdown
    payment_methods = {
        "Cash App": logs_filtered["Cash App"].sum(),
        "Zelle": logs_filtered["Zelle"].sum(),
        "PayPal": logs_filtered["PayPal"].sum(),
        "Bank Transfer": logs_filtered["Bank Transfer"].sum()
    }
    
    # Pie chart for payment methods
    fig = px.pie(
        values=list(payment_methods.values()),
        names=list(payment_methods.keys()),
        title="Payment Method Distribution",
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Payment method metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Cash App", f"${payment_methods['Cash App']:,.2f}")
    with col2:
        st.metric("⚡ Zelle", f"${payment_methods['Zelle']:,.2f}")
    with col3:
        st.metric("🅿️ PayPal", f"${payment_methods['PayPal']:,.2f}")
    with col4:
        st.metric("🏦 Bank Transfer", f"${payment_methods['Bank Transfer']:,.2f}")

st.markdown("---")

# ---------- Payout Confirmations ----------
st.subheader("✅ Payout Confirmations")

# Payout status filters
col1, col2 = st.columns([3, 1])
with col1:
    payout_status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Completed", "Processing", "Failed"],
        key="payout_status_filter"
    )
with col2:
    if st.button("🔄 Refresh Payouts"):
        st.session_state.payout_confirmations = generate_payout_confirmations()
        st.rerun()

# Filter payouts
filtered_payouts = payouts_df.copy()
if payout_status_filter != "All":
    filtered_payouts = filtered_payouts[filtered_payouts["Status"] == payout_status_filter]

# Format payout data
filtered_payouts["Amount"] = filtered_payouts["Amount"].apply(lambda x: f"${x:,.2f}")

# Color code status
def highlight_status(val):
    if "Completed" in str(val):
        return 'background-color: #d4edda; color: #155724'
    elif "Processing" in str(val):
        return 'background-color: #fff3cd; color: #856404'
    elif "Failed" in str(val):
        return 'background-color: #f8d7da; color: #721c24'
    return ''

st.dataframe(
    filtered_payouts.style.applymap(highlight_status, subset=['Status']),
    use_container_width=True,
    height=300
)

# Payout summary
col1, col2, col3 = st.columns(3)
with col1:
    completed_amount = payouts_df[payouts_df["Status"] == "Completed"]["Amount"].apply(
        lambda x: float(x.replace('$', '').replace(',', '')) if isinstance(x, str) else x
    ).sum()
    st.metric("✅ Completed Payouts", f"${completed_amount:,.2f}")

with col2:
    processing_count = len(payouts_df[payouts_df["Status"] == "Processing"])
    st.metric("⏳ Processing", processing_count)

with col3:
    failed_count = len(payouts_df[payouts_df["Status"] == "Failed"])
    st.metric("❌ Failed", failed_count)

st.markdown("---")

# ---------- Footer ----------
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #FF6B6B, #4ECDC4); color: white; border-radius: 10px; margin-top: 2rem;">
    <h3>🐉 Dragon Dash Sweepstakes</h3>
    <p>Professional Dashboard • Real-time Analytics • Secure Transactions</p>
    <p><em>Last Updated: {}</em></p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# ---------- Sidebar Additional Info ----------
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Quick Stats")
st.sidebar.info(f"**Total Clients:** {len(client_df)}")
st.sidebar.info(f"**Active Filters:** {len(client_df) - len(filtered_df)} hidden")
st.sidebar.info(f"**Data Generated:** {datetime.now().strftime('%Y-%m-%d')}")

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Actions")
if st.sidebar.button("🔄 Refresh All Data"):
    st.session_state.client_data = generate_demo_clients()
    st.session_state.daily_logs = generate_daily_logs()
    st.session_state.payout_confirmations = generate_payout_confirmations()
    st.rerun()

if st.sidebar.button("📋 Generate Report"):
    st.sidebar.success("Report generation feature coming soon!")

# ---------- Instructions ----------
with st.expander("ℹ️ How to Use This Dashboard"):
    st.markdown("""
    **Dragon Dash Dashboard Features:**
    
    1. **Client Management**: View all client accounts with verification status, balances, and transaction history
    2. **Transaction Tracking**: Monitor Cash App, Zelle, PayPal, and Bank Transfer amounts
    3. **Daily Analytics**: Track daily transaction volumes and trends
    4. **Payout Confirmations**: Manage and monitor payout status and confirmations
    5. **Filtering & Search**: Use sidebar filters and search to find specific clients or data
    6. **Export Data**: Download client data as CSV for external analysis
    
    **Navigation Tips:**
    - Use the sidebar filters to narrow down client data
    - Click on tabs to switch between different analytical views
    - Hover over charts for detailed information
    - Use the search bar to quickly find specific clients
    
    **Demo Data**: This dashboard uses realistic demo data for demonstration purposes.
    All client information is fictional and generated for testing purposes only.
    """)
