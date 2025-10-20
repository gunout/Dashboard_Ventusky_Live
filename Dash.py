# dashboard_ventusky_analytics.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
import time
from streamlit.components.v1 import html

# Configuration de la page
st.set_page_config(
    page_title="Ventusky & Analytics Météo Avancées",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #00aaff, #0066cc, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .alert-warning {
        background: linear-gradient(135deg, #ff9966, #ff5e62);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ff5e62;
    }
    .alert-info {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #4facfe;
    }
    .tab-container {
        background: rgba(255,255,255,0.95);
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

class AdvancedWeatherAnalytics:
    def __init__(self):
        self.weather_data = self.generate_sample_data()
        self.storm_tracks = self.generate_storm_data()
        
    def generate_sample_data(self):
        """Génère des données météorologiques simulées réalistes"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), 
                             end=datetime.now() + timedelta(days=3), freq='H')
        
        data = {
            'datetime': dates,
            'temperature': np.random.normal(25, 5, len(dates)) + np.sin(np.arange(len(dates)) * 0.1) * 8,
            'humidity': np.random.normal(65, 15, len(dates)),
            'pressure': np.random.normal(1013, 10, len(dates)),
            'wind_speed': np.random.gamma(2, 2, len(dates)) + np.abs(np.sin(np.arange(len(dates)) * 0.2)) * 15,
            'wind_direction': np.random.uniform(0, 360, len(dates)),
            'precipitation': np.random.exponential(0.5, len(dates)),
            'cloud_cover': np.random.uniform(0, 100, len(dates))
        }
        
        # Ajouter des tendances réalistes
        data['temperature'] += np.linspace(0, 3, len(dates))  # Réchauffement progressif
        data['pressure'] -= np.sin(np.arange(len(dates)) * 0.05) * 8  # Variations de pression
        
        return pd.DataFrame(data)
    
    def generate_storm_data(self):
        """Génère des données de suivi de tempêtes simulées"""
        storms = []
        for i in range(3):
            storm_start = datetime.now() - timedelta(hours=np.random.randint(6, 48))
            track_points = []
            
            lat, lon = np.random.uniform(-20, 20), np.random.uniform(40, 80)
            for j in range(12):
                track_points.append({
                    'datetime': storm_start + timedelta(hours=j*6),
                    'lat': lat + np.random.uniform(-1, 1),
                    'lon': lon + np.random.uniform(-1, 1),
                    'intensity': np.random.uniform(30, 120),
                    'category': self.get_storm_category(np.random.uniform(30, 120))
                })
            storms.append({
                'name': f"STORM-{chr(65+i)}",
                'track': track_points
            })
        return storms
    
    def get_storm_category(self, wind_speed):
        """Catégorise les tempêtes selon l'échelle de Beaufort"""
        if wind_speed >= 118:
            return "Ouragan"
        elif wind_speed >= 89:
            return "Tempête Violente"
        elif wind_speed >= 63:
            return "Tempête"
        elif wind_speed >= 50:
            return "Coup de vent"
        else:
            return "Vent fort"
    
    def create_weather_metrics(self):
        """Crée les métriques météorologiques principales"""
        current = self.weather_data.iloc[-1]
        previous = self.weather_data.iloc[-2]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            delta_temp = current['temperature'] - previous['temperature']
            st.metric("🌡️ Température", f"{current['temperature']:.1f}°C", 
                     f"{delta_temp:+.1f}°C")
        
        with col2:
            delta_wind = current['wind_speed'] - previous['wind_speed']
            st.metric("💨 Vitesse vent", f"{current['wind_speed']:.1f} km/h",
                     f"{delta_wind:+.1f} km/h")
        
        with col3:
            delta_pressure = current['pressure'] - previous['pressure']
            st.metric("📊 Pression", f"{current['pressure']:.1f} hPa",
                     f"{delta_pressure:+.1f} hPa")
        
        with col4:
            st.metric("💧 Humidité", f"{current['humidity']:.1f}%",
                     f"{(current['humidity'] - previous['humidity']):+.1f}%")
        
        with col5:
            st.metric("🌧️ Précipitation", f"{current['precipitation']:.1f} mm/h",
                     f"{(current['precipitation'] - previous['precipitation']):+.1f} mm")
    
    def create_temperature_analysis(self):
        """Analyse avancée des températures"""
        st.markdown("### 🌡️ Analyse des Températures")
        
        fig = make_subplots(rows=2, cols=1, 
                           subplot_titles=('Évolution Température', 'Cycle Journalier'),
                           vertical_spacing=0.1)
        
        # Graphique d'évolution
        fig.add_trace(
            go.Scatter(x=self.weather_data['datetime'], y=self.weather_data['temperature'],
                      name='Température', line=dict(color='red', width=2)),
            row=1, col=1
        )
        
        # Cycle journalier
        self.weather_data['hour'] = self.weather_data['datetime'].dt.hour
        daily_cycle = self.weather_data.groupby('hour')['temperature'].mean()
        
        fig.add_trace(
            go.Scatter(x=daily_cycle.index, y=daily_cycle.values,
                      name='Cycle Journalier', line=dict(color='orange', width=2)),
            row=2, col=1
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiques de température
        col1, col2, col3, col4 = st.columns(4)
        temp_data = self.weather_data['temperature']
        
        with col1:
            st.metric("Max 24h", f"{temp_data[-24:].max():.1f}°C")
        with col2:
            st.metric("Min 24h", f"{temp_data[-24:].min():.1f}°C")
        with col3:
            st.metric("Moyenne", f"{temp_data.mean():.1f}°C")
        with col4:
            st.metric("Écart-type", f"{temp_data.std():.1f}°C")
    
    def create_wind_analysis(self):
        """Analyse avancée du vent"""
        st.markdown("### 💨 Analyse des Vents")
        
        # Graphique de rose des vents
        recent_data = self.weather_data.tail(24)
        
        fig = px.scatter_polar(recent_data, r='wind_speed', theta='wind_direction',
                              color='wind_speed', size='wind_speed',
                              color_continuous_scale='viridis',
                              title='Rose des Vents (24h)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse des rafales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            max_wind = recent_data['wind_speed'].max()
            st.metric("Rafale Max", f"{max_wind:.1f} km/h")
        
        with col2:
            avg_wind = recent_data['wind_speed'].mean()
            st.metric("Vitesse Moyenne", f"{avg_wind:.1f} km/h")
        
        with col3:
            dominant_dir = recent_data['wind_direction'].mode().iloc[0] if not recent_data['wind_direction'].mode().empty else 0
            st.metric("Direction Dominante", f"{dominant_dir:.0f}°")
    
    def create_pressure_analysis(self):
        """Analyse des tendances de pression"""
        st.markdown("### 📊 Analyse Barométrique")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=self.weather_data['datetime'], 
                                y=self.weather_data['pressure'],
                                name='Pression', line=dict(color='blue', width=2)))
        
        # Ajouter une ligne de tendance
        z = np.polyfit(range(len(self.weather_data)), self.weather_data['pressure'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(x=self.weather_data['datetime'], 
                                y=p(range(len(self.weather_data))),
                                name='Tendance', line=dict(color='red', dash='dash')))
        
        fig.update_layout(title='Évolution de la Pression Atmosphérique',
                         yaxis_title='Pression (hPa)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Alertes de pression
        current_pressure = self.weather_data['pressure'].iloc[-1]
        pressure_change = self.weather_data['pressure'].iloc[-1] - self.weather_data['pressure'].iloc[-6]
        
        if pressure_change < -5:
            st.markdown('<div class="alert-warning">⚠️ Chute rapide de pression - Risque de détérioration météo</div>', 
                       unsafe_allow_html=True)
        elif pressure_change > 5:
            st.markdown('<div class="alert-info">📈 Hausse de pression - Amélioration météo attendue</div>', 
                       unsafe_allow_html=True)
    
    def create_storm_tracking(self):
        """Suivi des systèmes dépressionnaires"""
        st.markdown("### 🌀 Suivi des Systèmes Dépressionnaires")
        
        if not self.storm_tracks:
            st.info("Aucun système dépressionnaire significatif détecté")
            return
        
        for storm in self.storm_tracks:
            with st.expander(f"🌀 {storm['name']} - {storm['track'][-1]['category']}", expanded=True):
                # Créer la carte de trajectoire
                fig = go.Figure()
                
                lats = [point['lat'] for point in storm['track']]
                lons = [point['lon'] for point in storm['track']]
                intensities = [point['intensity'] for point in storm['track']]
                
                fig.add_trace(go.Scattermapbox(
                    lat=lats,
                    lon=lons,
                    mode='lines+markers',
                    marker=dict(size=8, color=intensities, colorscale='Viridis',
                               colorbar=dict(title="Intensité (km/h)")),
                    line=dict(width=3, color='red'),
                    text=[f"Vitesse: {intensity:.1f} km/h" for intensity in intensities],
                    hoverinfo='text'
                ))
                
                fig.update_layout(
                    mapbox=dict(
                        style="open-street-map",
                        center=dict(lat=np.mean(lats), lon=np.mean(lons)),
                        zoom=3
                    ),
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Détails de la tempête
                current_state = storm['track'][-1]
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Intensité actuelle", f"{current_state['intensity']:.1f} km/h")
                with col2:
                    st.metric("Catégorie", current_state['category'])
                with col3:
                    st.metric("Position", f"{current_state['lat']:.2f}°, {current_state['lon']:.2f}°")
                with col4:
                    next_update = current_state['datetime'] + timedelta(hours=6)
                    st.metric("Prochaine mise à jour", next_update.strftime("%H:%M"))
    
    def create_weather_forecast(self):
        """Prévisions météorologiques"""
        st.markdown("### 📈 Prévisions à 72 heures")
        
        forecast_data = self.weather_data.tail(72)
        
        fig = make_subplots(rows=2, cols=1, 
                           subplot_titles=('Température et Précipitations', 'Vent et Pression'),
                           vertical_spacing=0.1)
        
        # Température et précipitations
        fig.add_trace(
            go.Scatter(x=forecast_data['datetime'], y=forecast_data['temperature'],
                      name='Température', line=dict(color='red')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=forecast_data['datetime'], y=forecast_data['precipitation'],
                   name='Précipitation', marker_color='blue', opacity=0.6),
            row=1, col=1
        )
        
        # Vent et pression
        fig.add_trace(
            go.Scatter(x=forecast_data['datetime'], y=forecast_data['wind_speed'],
                      name='Vitesse vent', line=dict(color='green')),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=forecast_data['datetime'], y=forecast_data['pressure'],
                      name='Pression', line=dict(color='purple'), yaxis='y2'),
            row=2, col=1
        )
        
        fig.update_layout(height=500, showlegend=True)
        fig.update_yaxes(title_text="Pression (hPa)", secondary_y=True, row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_risk_assessment(self):
        """Évaluation des risques météorologiques"""
        st.markdown("### ⚠️ Évaluation des Risques")
        
        current = self.weather_data.iloc[-1]
        
        risks = []
        
        # Évaluation du risque vent
        if current['wind_speed'] > 60:
            risks.append(("💨 Vent violent", "Élevé", "Risque de dommages"))
        elif current['wind_speed'] > 40:
            risks.append(("💨 Vent fort", "Modéré", "Soyez prudent"))
        else:
            risks.append(("💨 Vent", "Faible", "Conditions normales"))
        
        # Évaluation du risque précipitations
        if current['precipitation'] > 10:
            risks.append(("🌧️ Pluie intense", "Élevé", "Risque d'inondation"))
        elif current['precipitation'] > 5:
            risks.append(("🌧️ Forte pluie", "Modéré", "Risque de ruissellement"))
        else:
            risks.append(("🌧️ Précipitations", "Faible", "Conditions normales"))
        
        # Évaluation du risque température
        if current['temperature'] > 35:
            risks.append(("🔥 Canicule", "Élevé", "Risque santé"))
        elif current['temperature'] < -5:
            risks.append(("❄️ Froid intense", "Élevé", "Risque santé"))
        else:
            risks.append(("🌡️ Température", "Faible", "Conditions normales"))
        
        # Afficher les risques
        for risk_name, level, description in risks:
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.write(risk_name)
            with col2:
                if level == "Élevé":
                    st.error(level)
                elif level == "Modéré":
                    st.warning(level)
                else:
                    st.success(level)
            with col3:
                st.write(description)

def create_ventusky_integration():
    """Crée l'intégration Ventusky"""
    
    ventusky_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ventusky Intégré</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background: #1e1e1e;
                color: white;
            }
            .browser-container {
                width: 100%;
                height: 700px;
                background: #2d2d2d;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            .browser-header {
                background: #3d3d3d;
                padding: 15px 20px;
                display: flex;
                align-items: center;
                gap: 15px;
                border-bottom: 1px solid #4d4d4d;
            }
            .browser-controls {
                display: flex;
                gap: 8px;
            }
            .control-btn {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                cursor: pointer;
            }
            .close { background: #ff5f57; }
            .minimize { background: #ffbd2e; }
            .maximize { background: #28ca42; }
            .url-display {
                flex: 1;
                background: #1e1e1e;
                border: 1px solid #4d4d4d;
                border-radius: 20px;
                padding: 10px 20px;
                color: white;
                font-size: 14px;
                margin: 0 20px;
            }
            .browser-actions {
                display: flex;
                gap: 12px;
            }
            .action-btn {
                background: #4d4d4d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s;
            }
            .action-btn:hover {
                background: #5d5d5d;
                transform: translateY(-1px);
            }
            .browser-content {
                height: calc(100% - 60px);
                background: white;
            }
            .ventusky-frame {
                width: 100%;
                height: 100%;
                border: none;
            }
            .status-bar {
                background: #3d3d3d;
                padding: 8px 20px;
                font-size: 12px;
                color: #ccc;
                border-top: 1px solid #4d4d4d;
                display: flex;
                justify-content: space-between;
            }
        </style>
    </head>
    <body>
        <div class="browser-container">
            <div class="browser-header">
                <div class="browser-controls">
                    <div class="control-btn close"></div>
                    <div class="control-btn minimize"></div>
                    <div class="control-btn maximize"></div>
                </div>
                <div class="url-display" id="urlDisplay">https://www.ventusky.com</div>
                <div class="browser-actions">
                    <button class="action-btn" onclick="refreshVentusky()">🔄</button>
                    <button class="action-btn" onclick="fullscreenVentusky()">📺</button>
                    <button class="action-btn" onclick="switchLayer('wind')">💨</button>
                    <button class="action-btn" onclick="switchLayer('temp')">🌡️</button>
                    <button class="action-btn" onclick="switchLayer('prec')">🌧️</button>
                </div>
            </div>
            <div class="browser-content">
                <iframe class="ventusky-frame" id="ventuskyFrame" 
                        src="https://www.ventusky.com"
                        allowfullscreen></iframe>
            </div>
            <div class="status-bar">
                <span id="statusText">Ventusky intégré - Surveillance active</span>
                <span id="connectionStatus">🟢 Connecté</span>
            </div>
        </div>

        <script>
        function refreshVentusky() {
            const frame = document.getElementById('ventuskyFrame');
            frame.src = frame.src;
            updateStatus('Actualisation en cours...');
        }

        function fullscreenVentusky() {
            const frame = document.getElementById('ventuskyFrame');
            if (frame.requestFullscreen) {
                frame.requestFullscreen();
            } else if (frame.webkitRequestFullscreen) {
                frame.webkitRequestFullscreen();
            } else if (frame.msRequestFullscreen) {
                frame.msRequestFullscreen();
            }
            updateStatus('Mode plein écran activé');
        }

        function switchLayer(layer) {
            const baseUrl = 'https://www.ventusky.com';
            const frame = document.getElementById('ventuskyFrame');
            
            const layers = {
                'wind': '?p=wind',
                'temp': '?p=temp', 
                'prec': '?p=prec',
                'pressure': '?p=press',
                'clouds': '?p=cloud'
            };
            
            frame.src = baseUrl + (layers[layer] || '');
            updateStatus(`Couche activée: ${layer}`);
        }

        function updateStatus(message) {
            document.getElementById('statusText').textContent = message;
            document.getElementById('connectionStatus').textContent = new Date().toLocaleTimeString();
        }

        // Surveillance de la connexion
        setInterval(() => {
            const frame = document.getElementById('ventuskyFrame');
            try {
                if (frame.contentWindow.location.href) {
                    document.getElementById('connectionStatus').textContent = '🟢 Connecté';
                }
            } catch (e) {
                document.getElementById('connectionStatus').textContent = '🟡 Chargement...';
            }
        }, 5000);

        // Mise à jour automatique toutes les 15 minutes
        setInterval(refreshVentusky, 900000);
        </script>
    </body>
    </html>
    """
    return ventusky_html

def main():
    st.markdown('<h1 class="main-header">🌪️ Ventusky & Analytics Météo Avancées</h1>', 
                unsafe_allow_html=True)
    
    # Initialisation des analytics
    analytics = AdvancedWeatherAnalytics()
    
    # Sidebar avec contrôles
    st.sidebar.markdown("## 🎛️ Contrôles Analytics")
    
    st.sidebar.markdown("### 📊 Paramètres d'analyse")
    analysis_period = st.sidebar.selectbox(
        "Période d'analyse:",
        ["24 heures", "48 heures", "7 jours", "30 jours"],
        index=0
    )
    
    auto_refresh = st.sidebar.checkbox("🔄 Actualisation automatique", value=True)
    refresh_interval = st.sidebar.selectbox("Intervalle:", [5, 10, 15, 30], index=1)
    
    st.sidebar.markdown("### ⚠️ Alertes")
    alert_wind = st.sidebar.slider("Seuil alerte vent (km/h):", 0, 100, 60)
    alert_rain = st.sidebar.slider("Seuil alerte pluie (mm/h):", 0, 50, 10)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📈 Métriques Temps Réel")
    
    # Métriques rapides dans la sidebar
    current_data = analytics.weather_data.iloc[-1]
    st.sidebar.metric("🌡️ Température", f"{current_data['temperature']:.1f}°C")
    st.sidebar.metric("💨 Vent", f"{current_data['wind_speed']:.1f} km/h")
    st.sidebar.metric("📊 Pression", f"{current_data['pressure']:.1f} hPa")
    st.sidebar.metric("💧 Humidité", f"{current_data['humidity']:.1f}%")
    
    # Navigation par onglets principale
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Ventusky Intégré", 
        "📊 Analytics Temps Réel", 
        "🌀 Suivi Tempêtes",
        "📈 Prévisions"
    ])
    
    with tab1:
        st.markdown("### 💨 Ventusky - Visualisation Météo Avancée")
        st.info("""
        **Ventusky offre une visualisation météorologique immersive avec:**
        - Animations fluides des conditions météo
        - Multiples couches de données (vent, température, précipitations)
        - Interface intuitive et responsive
        - Données globales en temps réel
        """)
        
        # Intégration Ventusky
        ventusky_html = create_ventusky_integration()
        html(ventusky_html, height=750, scrolling=False)
        
        # Conseils d'utilisation
        with st.expander("💡 Conseils d'utilisation Ventusky"):
            st.markdown("""
            **Pour une utilisation optimale:**
            - Utilisez les boutons 💨🌡️🌧️ pour changer de couche
            - Cliquez sur 📺 pour le mode plein écran
            - Actualisez régulièrement avec 🔄
            - Zoomez/dézoomez avec la molette souris
            - Cliquez-glissez pour vous déplacer sur la carte
            
            **Couches disponibles:**
            - **💨 Vent** - Visualisation des vents et courants
            - **🌡️ Température** - Cartes de températures
            - **🌧️ Précipitations** - Pluie, neige et précipitations
            - **📊 Pression** - Pressions atmosphériques
            - **☁️ Nuages** - Couverture nuageuse
            """)
    
    with tab2:
        st.markdown("### 📊 Analytics Météo Temps Réel")
        
        # Métriques principales
        analytics.create_weather_metrics()
        
        # Analyses avancées
        col1, col2 = st.columns([2, 1])
        
        with col1:
            analytics.create_temperature_analysis()
            analytics.create_pressure_analysis()
        
        with col2:
            analytics.create_wind_analysis()
            analytics.create_risk_assessment()
    
    with tab3:
        st.markdown("### 🌀 Suivi des Systèmes Dépressionnaires")
        analytics.create_storm_tracking()
        
        # Statistiques des tempêtes
        st.markdown("#### 📈 Statistiques des Tempêtes Actives")
        if analytics.storm_tracks:
            storm_stats = []
            for storm in analytics.storm_tracks:
                current = storm['track'][-1]
                storm_stats.append({
                    'Nom': storm['name'],
                    'Catégorie': current['category'],
                    'Intensité (km/h)': current['intensity'],
                    'Latitude': current['lat'],
                    'Longitude': current['lon']
                })
            
            stats_df = pd.DataFrame(storm_stats)
            st.dataframe(stats_df, use_container_width=True)
    
    with tab4:
        st.markdown("### 📈 Prévisions Météorologiques")
        analytics.create_weather_forecast()
        
        # Résumé des prévisions
        st.markdown("#### 📋 Résumé des Prévisions")
        
        forecast_summary = analytics.weather_data.tail(24)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            max_temp = forecast_summary['temperature'].max()
            st.metric("Max 24h", f"{max_temp:.1f}°C")
        
        with col2:
            min_temp = forecast_summary['temperature'].min()
            st.metric("Min 24h", f"{min_temp:.1f}°C")
        
        with col3:
            total_rain = forecast_summary['precipitation'].sum()
            st.metric("Pluie totale", f"{total_rain:.1f} mm")
        
        with col4:
            avg_wind = forecast_summary['wind_speed'].mean()
            st.metric("Vent moyen", f"{avg_wind:.1f} km/h")
    
    # Actualisation automatique
    if auto_refresh:
        time.sleep(refresh_interval * 60)
        st.rerun()

if __name__ == "__main__":
    main()