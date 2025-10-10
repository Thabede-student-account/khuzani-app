from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import io
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key in production

# Data dictionaries (same as before, with corrected coordinates)
users_data = {
    'Thabede': {'password': 'Thabede@2025', 'role': 'Administrator'},
    'Rodney': {'password': 'password', 'role': 'Administrator'},
    'Chantel': {'password': 'Velrie', 'role': 'Investor'},
    'Katlego': {'password': 'Machete', 'role': 'Researcher'}
}
production_data = [
    {'StatID': 1, 'Year': 2023, 'CountryID': 1, 'MineralID': 1, 'Production_tonnes': 100000, 'ExportValue_BillionUSD': 5.2},
    {'StatID': 2, 'Year': 2023, 'CountryID': 2, 'MineralID': 2, 'Production_tonnes': 120000, 'ExportValue_BillionUSD': 6.4},
    {'StatID': 3, 'Year': 2023, 'CountryID': 3, 'MineralID': 3, 'Production_tonnes': 50000, 'ExportValue_BillionUSD': 2.41},
    {'StatID': 4, 'Year': 2023, 'CountryID': 4, 'MineralID': 4, 'Production_tonnes': 200000, 'ExportValue_BillionUSD': 10},
    {'StatID': 5, 'Year': 2024, 'CountryID': 1, 'MineralID': 1, 'Production_tonnes': 110000, 'ExportValue_BillionUSD': 6.13},
    {'StatID': 6, 'Year': 2024, 'CountryID': 2, 'MineralID': 2, 'Production_tonnes': 130000, 'ExportValue_BillionUSD': 7.25},
    {'StatID': 7, 'Year': 2024, 'CountryID': 3, 'MineralID': 3, 'Production_tonnes': 200000, 'ExportValue_BillionUSD': 10.5},
    {'StatID': 8, 'Year': 2024, 'CountryID': 4, 'MineralID': 4, 'Production_tonnes': 210000, 'ExportValue_BillionUSD': 11}
]
minerals_data = [
    {'MineralID': 1, 'MineralName': 'Cobalt', 'Description': 'Used in batteries and alloys', 'MarketPriceUSD_per_tonne': 52000},
    {'MineralID': 2, 'MineralName': 'Lithium', 'Description': 'Essential for EV batteries', 'MarketPriceUSD_per_tonne': 70000},
    {'MineralID': 3, 'MineralName': 'Graphite', 'Description': 'Used in batteries and lubricants', 'MarketPriceUSD_per_tonne': 800},
    {'MineralID': 4, 'MineralName': 'Manganese', 'Description': 'Used in steel production', 'MarketPriceUSD_per_tonne': 2200}
]
countries_data = [
    {'CountryID': 1, 'CountryName': 'DRC (Congo)', 'GDP_BillionUSD': 55, 'MiningRevenue_BillionUSD': 12, 'KeyProjects': 'Cobalt expansion in Kolwezi'},
    {'CountryID': 2, 'CountryName': 'South Africa', 'GDP_BillionUSD': 350, 'MiningRevenue_BillionUSD': 25, 'KeyProjects': 'Bushveld Lithium Project'},
    {'CountryID': 3, 'CountryName': 'Mozambique', 'GDP_BillionUSD': 20, 'MiningRevenue_BillionUSD': 4, 'KeyProjects': 'Balama Graphite Project'},
    {'CountryID': 4, 'CountryName': 'Namibia', 'GDP_BillionUSD': 15, 'MiningRevenue_BillionUSD': 3, 'KeyProjects': 'Otjozondu Manganese Project'}
]
sites_data = [
    {'SiteID': 1, 'SiteName': 'Kolwezi Mine', 'CountryID': 1, 'MineralID': 1, 'Latitude': -10.7167, 'Longitude': 25.4667, 'Production_tonnes': 100000},
    {'SiteID': 2, 'SiteName': 'Bushveld Lithium Project', 'CountryID': 2, 'MineralID': 2, 'Latitude': -24.5, 'Longitude': 29.0, 'Production_tonnes': 120000},
    {'SiteID': 3, 'SiteName': 'Balama Graphite', 'CountryID': 3, 'MineralID': 3, 'Latitude': -13.3333, 'Longitude': 38.7667, 'Production_tonnes': 50000},
    {'SiteID': 4, 'SiteName': 'Otjozondu Manganese Project', 'CountryID': 4, 'MineralID': 4, 'Latitude': -20.13, 'Longitude': 16.13, 'Production_tonnes': 200000}
]
insights_data = []  # Initially empty

# Convert to DataFrames
user_df = pd.DataFrame([{'Role': v['role'], 'Username': k, 'Password': v['password']} for k, v in users_data.items()])
mineral_df = pd.DataFrame(minerals_data)
country_df = pd.DataFrame(countries_data)
production_df = pd.DataFrame(production_data)
sites_df = pd.DataFrame(sites_data)
insights_df = pd.DataFrame(insights_data, columns=['Username', 'Insight', 'Timestamp', 'MineralID', 'CountryID'])

# Save functions
def save_users():
    try:
        user_df.to_excel('Users.xlsx', index=False)
    except Exception as e:
        print(f"Error saving users: {e}")

def save_insights():
    try:
        insights_df.to_csv('insights.csv', index=False)
    except Exception as e:
        print(f"Error saving insights: {e}")

# Authentication
def authenticate(username, password):
    if username in users_data and users_data[username]['password'] == password:
        return users_data[username]['role']
    return None

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    role = authenticate(username, password)
    if role:
        session['username'] = username
        session['role'] = role
        return redirect(url_for(f'{role.lower()}_dashboard'))
    return render_template('login.html', error="Invalid username or password.")

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'Administrator':
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html', username=session['username'])

@app.route('/investor_dashboard')
def investor_dashboard():
    if session.get('role') != 'Investor':
        return redirect(url_for('index'))
    return render_template('investor_dashboard.html', username=session['username'])

@app.route('/researcher_dashboard')
def researcher_dashboard():
    if session.get('role') != 'Researcher':
        return redirect(url_for('index'))
    return render_template('researcher_dashboard.html', username=session['username'])

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if session.get('role') != 'Administrator':
        return redirect(url_for('index'))
    global user_df
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            if username and password and role in ['Administrator', 'Investor', 'Researcher']:
                if username not in users_data:
                    users_data[username] = {'password': password, 'role': role}
                    user_df = pd.concat([user_df, pd.DataFrame({'Role': [role], 'Username': [username], 'Password': [password]})], ignore_index=True)
                    save_users()
                    return render_template('manage_users.html', message="User added successfully.", users=user_df.to_dict('records'))
                return render_template('manage_users.html', error="Username already exists.", users=user_df.to_dict('records'))
            return render_template('manage_users.html', error="All fields required or invalid role.", users=user_df.to_dict('records'))
        elif action == 'edit':
            username = request.form['username']
            password = request.form.get('password')
            role = request.form.get('role')
            if username in users_data:
                if password:
                    users_data[username]['password'] = password
                    user_df.loc[user_df['Username'] == username, 'Password'] = password
                if role in ['Administrator', 'Investor', 'Researcher']:
                    users_data[username]['role'] = role
                    user_df.loc[user_df['Username'] == username, 'Role'] = role
                save_users()
                return render_template('manage_users.html', message="User updated successfully.", users=user_df.to_dict('records'))
            return render_template('manage_users.html', error="User not found.", users=user_df.to_dict('records'))
        elif action == 'delete':
            username = request.form['username']
            if username in users_data:
                del users_data[username]
                user_df = user_df[user_df['Username'] != username]
                save_users()
                return render_template('manage_users.html', message="User deleted successfully.", users=user_df.to_dict('records'))
            return render_template('manage_users.html', error="User not found.", users=user_df.to_dict('records'))
    return render_template('manage_users.html', users=user_df.to_dict('records'))

@app.route('/edit_data', methods=['GET', 'POST'])
def edit_data():
    if session.get('role') != 'Administrator':
        return redirect(url_for('index'))
    global mineral_df, country_df, production_df
    if request.method == 'POST':
        action = request.form.get('action')
        data_type = request.form.get('data_type')
        data_id = request.form.get('data_id')
        new_value = request.form.get('new_value')
        try:
            data_id = int(data_id)
            if action == 'edit':
                if data_type == 'Mineral' and not mineral_df[mineral_df['MineralID'] == data_id].empty:
                    if new_value:
                        mineral_df.loc[mineral_df['MineralID'] == data_id, 'MarketPriceUSD_per_tonne'] = float(new_value)
                        return render_template('edit_data.html', message="Mineral updated.")
                    return render_template('edit_data.html', error="New value required.")
                elif data_type == 'Country' and not country_df[country_df['CountryID'] == data_id].empty:
                    if new_value:
                        country_df.loc[country_df['CountryID'] == data_id, 'GDP_BillionUSD'] = float(new_value)
                        return render_template('edit_data.html', message="Country updated.")
                    return render_template('edit_data.html', error="New value required.")
                elif data_type == 'Production' and not production_df[production_df['StatID'] == data_id].empty:
                    if new_value:
                        production_df.loc[production_df['StatID'] == data_id, 'Production_tonnes'] = float(new_value)
                        return render_template('edit_data.html', message="Production updated.")
                    return render_template('edit_data.html', error="New value required.")
                return render_template('edit_data.html', error="ID not found.")
            elif action == 'delete':
                if data_type == 'Mineral' and not mineral_df[mineral_df['MineralID'] == data_id].empty:
                    mineral_df = mineral_df[mineral_df['MineralID'] != data_id]
                    return render_template('edit_data.html', message="Mineral deleted.")
                elif data_type == 'Country' and not country_df[country_df['CountryID'] == data_id].empty:
                    country_df = country_df[country_df['CountryID'] != data_id]
                    return render_template('edit_data.html', message="Country deleted.")
                elif data_type == 'Production' and not production_df[production_df['StatID'] == data_id].empty:
                    production_df = production_df[production_df['StatID'] != data_id]
                    return render_template('edit_data.html', message="Production deleted.")
                return render_template('edit_data.html', error="ID not found.")
        except ValueError:
            return render_template('edit_data.html', error="Invalid ID or value.")
    return render_template('edit_data.html')

@app.route('/view_country_profiles', methods=['GET', 'POST'])
def view_country_profiles():
    if session.get('role') != 'Investor':
        return redirect(url_for('index'))
    if request.method == 'POST':
        country_name = request.form['country']
        country_row = country_df[country_df['CountryName'].str.lower() == country_name.lower()]
        if not country_row.empty:
            country_id = country_row['CountryID'].iloc[0]
            prod_data = production_df[production_df['CountryID'] == country_id].merge(mineral_df[['MineralID', 'MineralName']], on='MineralID')
            return render_template('country_profile.html', country=country_row.to_dict('records')[0], prod_data=prod_data.to_dict('records'))
        return render_template('view_country_profiles.html', error="Country not found.", countries=country_df['CountryName'].tolist())
    return render_template('view_country_profiles.html', countries=country_df['CountryName'].tolist())

@app.route('/view_charts', methods=['GET', 'POST'])
def view_charts():
    if session.get('role') != 'Investor':
        return redirect(url_for('index'))
    if request.method == 'POST':
        mineral_name = request.form['mineral']
        chart_type = request.form['chart_type']
        mineral_row = mineral_df[mineral_df['MineralName'].str.lower() == mineral_name.lower()]
        if not mineral_row.empty:
            mineral_id = mineral_row['MineralID'].iloc[0]
            prod_data = production_df[production_df['MineralID'] == mineral_id].merge(country_df[['CountryID', 'CountryName']], on='CountryID')
            if not prod_data.empty:
                if 'Production Trends' in chart_type:
                    fig = px.line(prod_data, x='Year', y='Production_tonnes', color='CountryName', title=f'{mineral_name} Production Trends')
                elif 'Export Value Trends' in chart_type:
                    fig = px.line(prod_data, x='Year', y='ExportValue_BillionUSD', color='CountryName', title=f'{mineral_name} Export Value Trends')
                elif 'Production Bar' in chart_type:
                    fig = px.bar(prod_data, x='Year', y='Production_tonnes', color='CountryName', title=f'{mineral_name} Production Bar Chart')
                elif 'Export Bar' in chart_type:
                    fig = px.bar(prod_data, x='Year', y='ExportValue_BillionUSD', color='CountryName', title=f'{mineral_name} Export Value Bar Chart')
                else:
                    return render_template('view_charts.html', error="Invalid chart type.", minerals=mineral_df['MineralName'].tolist())
                chart_div = fig.to_html(full_html=False)
                return render_template('view_charts.html', chart=chart_div, minerals=mineral_df['MineralName'].tolist())
            return render_template('view_charts.html', error="No production data for this mineral.", minerals=mineral_df['MineralName'].tolist())
        return render_template('view_charts.html', error="Mineral not found.", minerals=mineral_df['MineralName'].tolist())
    return render_template('view_charts.html', minerals=mineral_df['MineralName'].tolist())

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    if session.get('role') not in ['Administrator', 'Investor', 'Researcher']:
        return redirect(url_for('index'))
    if request.method == 'POST':
        data_type = request.form['data_type']
        name = request.form['name']
        if data_type == 'Mineral':
            row = mineral_df[mineral_df['MineralName'].str.lower() == name.lower()]
            if not row.empty:
                mineral_id = row['MineralID'].iloc[0]
                prod_data = production_df[production_df['MineralID'] == mineral_id].merge(country_df[['CountryID', 'CountryName']], on='CountryID')
                return render_template('view_data_result.html', data_type=data_type, name=name, data=row.to_dict('records'), prod_data=prod_data.to_dict('records'))
            return render_template('view_data.html', error="Mineral not found.", data_types=['Mineral', 'Country'], names=mineral_df['MineralName'].tolist())
        elif data_type == 'Country':
            row = country_df[country_df['CountryName'].str.lower() == name.lower()]
            if not row.empty:
                country_id = row['CountryID'].iloc[0]
                prod_data = production_df[production_df['CountryID'] == country_id].merge(mineral_df[['MineralID', 'MineralName']], on='MineralID')
                return render_template('view_data_result.html', data_type=data_type, name=name, data=row.to_dict('records'), prod_data=prod_data.to_dict('records'))
            return render_template('view_data.html', error="Country not found.", data_types=['Mineral', 'Country'], names=country_df['CountryName'].tolist())
        return render_template('view_data.html', error="Invalid data type.", data_types=['Mineral', 'Country'], names=[])
    return render_template('view_data.html', data_types=['Mineral', 'Country'], names=[])

@app.route('/export_data', methods=['GET', 'POST'])
def export_data():
    if session.get('role') != 'Researcher':
        return redirect(url_for('index'))
    if request.method == 'POST':
        data_type = request.form['data_type']
        buffer = io.BytesIO()
        if data_type == 'Mineral':
            mineral_df.to_csv(buffer, index=False)
        elif data_type == 'Country':
            country_df.to_csv(buffer, index=False)
        elif data_type == 'Production':
            production_df.to_csv(buffer, index=False)
        else:
            return render_template('export_data.html', error="Invalid data type.")
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"{data_type}_export.csv", mimetype='text/csv')
    return render_template('export_data.html')

@app.route('/add_insight', methods=['GET', 'POST'])
def add_insight():
    if session.get('role') != 'Researcher':
        return redirect(url_for('index'))
    global insights_df
    if request.method == 'POST':
        insight = request.form['insight']
        mineral_name = request.form['mineral']
        country_name = request.form['country']
        if not insight:
            return render_template('add_insight.html', error="Insight is required.", minerals=[''] + mineral_df['MineralName'].tolist(), countries=[''] + country_df['CountryName'].tolist())
        mineral_id = None
        country_id = None
        if mineral_name:
            row = mineral_df[mineral_df['MineralName'].str.lower() == mineral_name.lower()]
            if not row.empty:
                mineral_id = row['MineralID'].iloc[0]
        if country_name:
            row = country_df[country_df['CountryName'].str.lower() == country_name.lower()]
            if not row.empty:
                country_id = row['CountryID'].iloc[0]
        new_insight = pd.DataFrame({
            'Username': [session['username']],
            'Insight': [insight],
            'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'MineralID': [mineral_id],
            'CountryID': [country_id]
        })
        insights_df = pd.concat([insights_df, new_insight], ignore_index=True)
        save_insights()
        return render_template('add_insight.html', message="Insight added.", minerals=[''] + mineral_df['MineralName'].tolist(), countries=[''] + country_df['CountryName'].tolist())
    return render_template('add_insight.html', minerals=[''] + mineral_df['MineralName'].tolist(), countries=[''] + country_df['CountryName'].tolist())

@app.route('/view_interactive_map')
def view_interactive_map():
    if session.get('role') not in ['Administrator', 'Investor', 'Researcher']:
        return redirect(url_for('index'))
    m = folium.Map(location=[-2, 20], zoom_start=3)
    marker_cluster = MarkerCluster().add_to(m)
    for _, site in sites_df.iterrows():
        mineral = mineral_df[mineral_df['MineralID'] == site['MineralID']]['MineralName'].iloc[0]
        country = country_df[country_df['CountryID'] == site['CountryID']]['CountryName'].iloc[0]
        popup_text = f"{site['SiteName']}<br>{country}<br>{mineral}<br>Production: {site['Production_tonnes']} tonnes"
        folium.Marker(
            location=[site['Latitude'], site['Longitude']],
            popup=popup_text,
            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)
    map_html = m._repr_html_()
    return render_template('view_map.html', map_html=map_html)

@app.route('/view_insights')
def view_insights():
    if session.get('role') not in ['Administrator', 'Investor', 'Researcher']:
        return redirect(url_for('index'))
    insights_with_names = insights_df.copy()
    insights_with_names['MineralName'] = insights_with_names['MineralID'].map(mineral_df.set_index('MineralID')['MineralName'])
    insights_with_names['CountryName'] = insights_with_names['CountryID'].map(country_df.set_index('CountryID')['CountryName'])
    return render_template('view_insights.html', insights=insights_with_names.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)
