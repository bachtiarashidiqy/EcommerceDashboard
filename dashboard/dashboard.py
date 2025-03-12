import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="https://raw.githubusercontent.com/bachtiarashidiqy/EcommerceDashboard/master/dashboard/logo.png",
)

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/bachtiarashidiqy/EcommerceDashboard/master/dashboard/main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

main_df = load_data()

st.sidebar.image("https://raw.githubusercontent.com/bachtiarashidiqy/EcommerceDashboard/master/dashboard/logo.png", width=200)
st.sidebar.header("Data Filter")
start_date = st.sidebar.date_input("Start Date", main_df['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("End Date", main_df['order_purchase_timestamp'].max())

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
filtered_df = main_df[(main_df['order_purchase_timestamp'] >= start_date) & (main_df['order_purchase_timestamp'] <= end_date)]

def configure_bar_plot(ax, fig, title, description, top_values, highest_value, metric):
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)

    fmt = '{x:,.0f}'
    tick = ticker.StrMethodFormatter(fmt)
    ax.xaxis.set_major_formatter(tick)

    ax.set_xlabel('')
    ax.set_ylabel('')

    fig.text(0.09, 1.08, title, fontsize=20, fontweight='bold', fontfamily='serif')
    fig.text(0.09, 1.03, description, fontsize=15, fontweight='light', fontfamily='serif')

    highest = highest_value * 0.05 if metric == 'num_orders' else highest_value * 0.03

    for i, val in enumerate(top_values):
        ax.annotate(f"{val:,.0f}" if metric == 'num_orders' else f"{val:,.0f}", xy=(val + highest, i), va='center', ha='center', fontweight='light', fontfamily='serif', fontsize=14)

    ax.tick_params(axis='both', which='major', labelsize=14)

def plot_top_bottom_products(df, metric, title, description):
    best_selling_product = df.groupby('product_name').agg(
        num_orders=('order_id', 'nunique'),
        revenue=('payment_value', 'sum')
    ).sort_values(metric, ascending=False)

    top_10 = best_selling_product.head(10)
    bottom_10 = best_selling_product.tail(10).sort_values(metric, ascending=True)

    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

    color_map = ['#f5f5f1' for _ in range(10)]
    color_map[:3] = ['#FFB200', '#FFB200', '#FFB200']

    sns.barplot(y=top_10.index, x='num_orders' if metric == 'num_orders' else 'revenue', data=top_10, palette=color_map, edgecolor='darkgray', linewidth=0.6, ax=ax[0], orient='h')
    sns.barplot(y=bottom_10.index, x='num_orders' if metric == 'num_orders' else 'revenue', data=bottom_10, palette=color_map, edgecolor='darkgray', linewidth=0.6, ax=ax[1], orient='h')

    configure_bar_plot(ax[0], fig, title, description, top_10['num_orders' if metric == 'num_orders' else 'revenue'], top_10['num_orders' if metric == 'num_orders' else 'revenue'].max(), metric)
    configure_bar_plot(ax[1], fig, title, description, bottom_10['num_orders' if metric == 'num_orders' else 'revenue'], bottom_10['num_orders' if metric == 'num_orders' else 'revenue'].max(), metric)

    if metric == 'revenue':
        ax[0].tick_params(axis='x', labelrotation=45)
        ax[1].tick_params(axis='x', labelrotation=45)

    plt.tight_layout()
    st.pyplot(fig)

def plot_top_cities_states(df, group_by, title, description):
    top10 = df.groupby(group_by).agg(
        num_orders=('order_id', 'nunique'),
        revenue=('payment_value', 'sum')
    ).sort_values('revenue', ascending=False).head(10)

    fig, ax = plt.subplots(1, 2, figsize=(25, 15), dpi=300, sharey=True)

    color_map = ['#f5f5f1' for _ in range(10)]
    color_map[:3] = ['#FFB200', '#FFB200', '#FFB200']

    sns.barplot(y=top10.index, x='num_orders', data=top10, palette=color_map, edgecolor='darkgrey', linewidth=0.6, ax=ax[0], orient='h')
    sns.barplot(y=top10.index, x='revenue', data=top10, palette=color_map, edgecolor='darkgrey', linewidth=0.6, ax=ax[1], orient='h')

    configure_bar_plot(ax[0], fig, title, description, top10['num_orders'], top10['num_orders'].max(), 'num_orders')
    configure_bar_plot(ax[1], fig, title, description, top10['revenue'], top10['revenue'].max(), 'revenue')

    plt.tight_layout()
    st.pyplot(fig)

def plot_delivery_status(df):
    fig, ax = plt.subplots(figsize=(12, 7))
    values = df.arrival_status.value_counts().values
    labels = df.arrival_status.value_counts().index
    ax.pie(values, labels=labels, autopct='%1.1f%%', explode=(0.05, 0.05), colors=('#FFB200', '#C0C0C0'), textprops={'fontsize': 14})

    fig.text(0.05, 0.95, 'Number of On-Time and Late Deliveries to Customers', fontsize=18, fontweight='bold', fontfamily='serif', verticalalignment='top')
    fig.text(0.05, 0.90, 'Illustrates the distribution of on-time and late customer shipments', fontsize=14, fontweight='light', fontfamily='serif', verticalalignment='top')

    plt.tight_layout(rect=(0, 0, 1, 0.9))
    st.pyplot(fig)

st.title("E-Commerce Analytics Dashboard")

st.header("Product Analysis")
plot_top_bottom_products(filtered_df, 'num_orders', 'Top and Bottom 10 Products Ranked by Order Volume', 'Figure 1 presents the 10 products with the greatest number of orders\nFigure 2 presents the 10 products with the fewest number of orders')
plot_top_bottom_products(filtered_df, 'revenue', 'Top and Bottom 10 Products Ranked by Revenue', 'Figure 1 presents the 10 products with the highest revenue\nFigure 2 presents the 10 products with the lowest revenue')

st.header("Geographic Analysis")
plot_top_cities_states(filtered_df, 'customer_city', 'Top 10 Cities Ranked by Number of Orders and Revenue', 'This figure displays top 10 cities by its number of orders and Revenue')
plot_top_cities_states(filtered_df, 'customer_state', 'Top 10 States Ranked by Number of Orders and Revenue', 'This figure displays top 10 States by its number of orders and Revenue')

st.header("Delivery Analysis")
plot_delivery_status(filtered_df)


st.sidebar.markdown("""
<div style="text-align: center; margin-top: 20px;">
    <small><a href="https://www.linkedin.com/in/bachtiar-rian/" target="_blank">R Bachtiar Ashidiqy</a></small>
</div>
""", unsafe_allow_html=True)
