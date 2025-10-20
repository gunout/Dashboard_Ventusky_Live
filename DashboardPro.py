# dashboard_ventusky_pro_enhanced.py
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
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Ventusky Pro+ - Analytics Météo Avancées",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avancé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #00aaff, #0066cc, #0099ff, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        text-shadow: 0 4px 8px rgba(0,0,0,0.2);
        animation: gradient-shift 3s ease-in-out infinite;
    }
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.2);
    }
    .alert-critical {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 6px solid #ff0000;
        animation: pulse-alert 2s infinite;
    }
    .alert-warning {
        background: linear-gradient(135deg, #f7971e, #ffd200);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 6px solid #ff8c00;
    }
    .alert-info {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 6px solid #4facfe;
    }
    @keyframes pulse-alert {
        0% { transform: scale(1); box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
        50% { transform: scale(1.02); box-shadow: 0 0 30px rgba(255, 0, 0, 0.8); }
        100% { transform: scale(1); box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
    }
    .tab-container {
        background: rgba(255,255,255,0.98);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #f0f2f6;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background-color: #e0e0e0;
        border-radius: 8px;
        gap: 1px;
        padding: 16px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00aaff, #0066cc);
        color: white;
        box-shadow: 0 4px 12px rgba(0,170,255,0.3);
    }
    .weather-icon {
        font-size: 2rem;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

class EnhancedWeatherAnalytics:
    def __init__(self):
        self.weather_data = self.generate_enhanced_sample_data()
        self.storm_tracks = self.generate_enhanced_storm_data()
        self.ai_predictions = self.generate_ai_predictions()
        self.weather_alerts = self.generate_weather_alerts()
        
    def generate_enhanced_sample_data(self):
        """Génère des données météorologiques simulées plus réalistes et détaillées"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=14), 
                             end=datetime.now() + timedelta(days=7), freq='H')
        
        # Génération de données plus réalistes avec saisonnalité
        time_index = np.arange(len(dates))
        
        data = {
            'datetime': dates,
            'temperature': self.generate_realistic_temperature(time_index, len(dates)),
            'humidity': np.clip(np.random.normal(65, 12, len(dates)) + np.sin(time_index * 0.05) * 10, 20, 95),
            'pressure': np.random.normal(1013, 8, len(dates)) + np.sin(time_index * 0.02) * 5,
            'wind_speed': self.generate_realistic_wind_speed(time_index, len(dates)),
            'wind_direction': (np.cumsum(np.random.normal(0, 10, len(dates))) % 360),
            'precipitation': self.generate_realistic_precipitation(time_index, len(dates)),
            'cloud_cover': np.clip(np.random.normal(50, 25, len(dates)) + np.sin(time_index * 0.03) * 20, 0, 100),
            'visibility': np.clip(np.random.normal(15, 5, len(dates)) - np.random.exponential(0.5, len(dates)) * 10, 1, 30),
            'uv_index': np.clip(np.abs(np.sin(time_index * 0.1)) * 10 + np.random.normal(0, 1, len(dates)), 0, 12),
            'dew_point': np.random.normal(15, 5, len(dates)) + np.sin(time_index * 0.05) * 3,
            'feels_like': np.random.normal(25, 6, len(dates)),
            'gust_speed': np.random.gamma(3, 2, len(dates)) + 5
        }
        
        # Calcul de l'indice de chaleur
        data['heat_index'] = self.calculate_heat_index(data['temperature'], data['humidity'])
        
        return pd.DataFrame(data)
    
    def generate_realistic_temperature(self, time_index, n):
        """Génère des températures réalistes avec cycle jour/nuit et tendance"""
        base_temp = 25 + np.sin(time_index * 0.01) * 2  # Tendance saisonnière lente
        daily_cycle = np.sin(time_index * 2 * np.pi / 24) * 8  # Cycle jour/nuit
        noise = np.random.normal(0, 1.5, n)
        return base_temp + daily_cycle + noise
    
    def generate_realistic_wind_speed(self, time_index, n):
        """Génère des vitesses de vent réalistes avec rafales"""
        base_wind = np.random.gamma(1.5, 2, n) + 3
        gusts = np.random.exponential(0.3, n) * 15
        daily_variation = np.sin(time_index * 2 * np.pi / 24) * 2
        return np.maximum(base_wind + gusts + daily_variation, 0)
    
    def generate_realistic_precipitation(self, time_index, n):
        """Génère des précipitations réalistes avec événements de pluie"""
        # Probabilité de pluie plus élevée la nuit
        rain_prob = 0.3 + np.sin(time_index * 2 * np.pi / 24) * 0.2
        rain_events = np.random.binomial(1, rain_prob, n)
        intensity = np.random.exponential(2, n)
        return rain_events * intensity
    
    def calculate_heat_index(self, temperature, humidity):
        """Calcule l'indice de chaleur (heat index)"""
        # Formule simplifiée de l'indice de chaleur
        return temperature + 0.5 * (humidity / 100) * (temperature - 20)
    
    def generate_enhanced_storm_data(self):
        """Génère des données de tempêtes plus réalistes avec modèles de trajectoire"""
        storms = []
        storm_names = ["ATLANTIC-01", "PACIFIC-ALPHA", "INDIAN-DELTA"]
        
        for i, name in enumerate(storm_names):
            storm_start = datetime.now() - timedelta(hours=np.random.randint(12, 72))
            track_points = []
            
            # Point de départ réaliste selon le bassin
            if "ATLANTIC" in name:
                lat, lon = np.random.uniform(10, 30), np.random.uniform(-80, -40)
            elif "PACIFIC" in name:
                lat, lon = np.random.uniform(5, 25), np.random.uniform(120, 160)
            else:
                lat, lon = np.random.uniform(-15, 5), np.random.uniform(50, 90)
            
            for j in range(24):  # 6 jours de prévision
                # Modèle de mouvement réaliste
                lat += np.random.uniform(-0.3, 0.3)
                lon += np.random.uniform(-0.4, 0.4)
                
                # Intensité qui évolue de manière réaliste
                if j < 8:
                    intensity = np.random.uniform(30, 80)  # Phase de développement
                elif j < 16:
                    intensity = np.random.uniform(80, 140)  # Phase mature
                else:
                    intensity = np.random.uniform(40, 100)  # Phase d'affaiblissement
                
                track_points.append({
                    'datetime': storm_start + timedelta(hours=j*6),
                    'lat': lat,
                    'lon': lon,
                    'intensity': intensity,
                    'category': self.get_storm_category(intensity),
                    'pressure': 1010 - (intensity / 5),
                    'radius': intensity * 0.5 + np.random.uniform(50, 150)
                })
            storms.append({
                'name': name,
                'track': track_points,
                'current_threat': np.random.choice(['Faible', 'Modéré', 'Élevé'], p=[0.3, 0.5, 0.2])
            })
        return storms
    
    def get_storm_category(self, wind_speed):
        """Catégorise les tempêtes selon l'échelle de Saffir-Simpson améliorée"""
        if wind_speed >= 252:
            return "Catégorie 5"
        elif wind_speed >= 209:
            return "Catégorie 4"
        elif wind_speed >= 178:
            return "Catégorie 3"
        elif wind_speed >= 154:
            return "Catégorie 2"
        elif wind_speed >= 119:
            return "Catégorie 1"
        elif wind_speed >= 63:
            return "Tempête Tropicale"
        else:
            return "Dépression Tropicale"
    
    def generate_ai_predictions(self):
        """Génère des prédictions IA simulées"""
        current_time = datetime.now()
        predictions = {
            'short_term': {
                'next_6h': {
                    'trend': 'stable',
                    'confidence': 0.85,
                    'details': 'Conditions stables avec vent modéré'
                },
                'next_12h': {
                    'trend': 'deteriorating', 
                    'confidence': 0.72,
                    'details': 'Arrivée d\'un front froid avec pluies'
                }
            },
            'storm_development': {
                'probability': 0.45,
                'expected_intensity': 'Modérée',
                'timeline': '24-48 heures'
            },
            'anomalies': [
                'Pression anormalement basse dans le secteur Nord',
                'Augmentation rapide de l\'humidité',
                'Variations de vent inhabituelles'
            ]
        }
        return predictions
    
    def generate_weather_alerts(self):
        """Génère des alertes météorologiques avancées"""
        alerts = [
            {
                'type': 'VIGILANCE_ORANGE',
                'title': 'Vent violent',
                'region': 'Côtes Nord',
                'severity': 'Élevée',
                'start_time': datetime.now(),
                'end_time': datetime.now() + timedelta(hours=12),
                'description': 'Rafales attendues jusqu\'à 90 km/h',
                'impact': 'Transport maritime perturbé',
                'actions': 'Éviter les zones côtières'
            },
            {
                'type': 'VIGILANCE_JAUNE',
                'title': 'Fortes précipitations',
                'region': 'Secteur Est', 
                'severity': 'Modérée',
                'start_time': datetime.now() + timedelta(hours=6),
                'end_time': datetime.now() + timedelta(hours=18),
                'description': 'Cumuls attendus: 40-60 mm',
                'impact': 'Risque de ruissellement',
                'actions': 'Surveillance des cours d\'eau'
            }
        ]
        return alerts
    
    def create_advanced_metrics_dashboard(self):
        """Crée un tableau de bord de métriques avancées"""
        current = self.weather_data.iloc[-1]
        previous = self.weather_data.iloc[-2]
        
        # Métriques principales avec tendances
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            delta_temp = current['temperature'] - previous['temperature']
            trend_icon = "📈" if delta_temp > 0 else "📉" if delta_temp < 0 else "➡️"
            st.metric("🌡️ Température", f"{current['temperature']:.1f}°C", 
                     f"{trend_icon} {delta_temp:+.1f}°C")
        
        with col2:
            delta_wind = current['wind_speed'] - previous['wind_speed']
            st.metric("💨 Vent Moyen", f"{current['wind_speed']:.1f} km/h",
                     f"{delta_wind:+.1f} km/h")
            st.metric("💨 Rafales", f"{current['gust_speed']:.1f} km/h")
        
        with col3:
            delta_pressure = current['pressure'] - previous['pressure']
            pressure_trend = "📉" if delta_pressure < -2 else "📈" if delta_pressure > 2 else "➡️"
            st.metric("📊 Pression", f"{current['pressure']:.1f} hPa",
                     f"{pressure_trend} {delta_pressure:+.1f} hPa")
        
        with col4:
            heat_index = current['heat_index']
            risk_level = "⚠️" if heat_index > 30 else "✅"
            st.metric("🔥 Indice Chaleur", f"{heat_index:.1f}°C", risk_level)
            st.metric("💧 Point Rosée", f"{current['dew_point']:.1f}°C")
        
        with col5:
            st.metric("🌧️ Précipitation", f"{current['precipitation']:.1f} mm/h")
            st.metric("👁️ Visibilité", f"{current['visibility']:.1f} km")
    
    def create_ai_weather_analysis(self):
        """Analyse météo avancée avec insights IA"""
        st.markdown("### 🧠 IA Météo - Analyse Prédictive")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Graphique d'analyse de tendances
            fig = make_subplots(rows=2, cols=1, 
                               subplot_titles=('Analyse Multi-Variables', 'Indices de Confort'),
                               vertical_spacing=0.12)
            
            # Variables principales
            recent_data = self.weather_data.tail(48)
            fig.add_trace(
                go.Scatter(x=recent_data['datetime'], y=recent_data['temperature'],
                          name='Température', line=dict(color='red', width=3)),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=recent_data['datetime'], y=recent_data['pressure'],
                          name='Pression', line=dict(color='blue', width=2), yaxis='y2'),
                row=1, col=1
            )
            
            # Indices de confort
            fig.add_trace(
                go.Scatter(x=recent_data['datetime'], y=recent_data['heat_index'],
                          name='Indice Chaleur', line=dict(color='orange', width=2)),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=recent_data['datetime'], y=recent_data['dew_point'],
                          name='Point Rosée', line=dict(color='green', width=2)),
                row=2, col=1
            )
            
            fig.update_layout(height=500, showlegend=True)
            fig.update_yaxes(title_text="Pression (hPa)", secondary_y=True, row=1, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Insights IA
            st.markdown("#### 📋 Insights IA")
            
            st.markdown("##### 🔮 Prévisions Court Terme")
            for period, prediction in self.ai_predictions['short_term'].items():
                with st.container():
                    st.write(f"**{period.replace('_', ' ').title()}**")
                    st.write(f"Tendance: {prediction['trend']}")
                    st.write(f"Confiance: {prediction['confidence']*100}%")
                    st.write(prediction['details'])
                    st.progress(prediction['confidence'])
                    st.markdown("---")
            
            st.markdown("##### ⚠️ Anomalies Détectées")
            for anomaly in self.ai_predictions['anomalies']:
                st.write(f"• {anomaly}")
    
    def create_advanced_storm_analytics(self):
        """Analytics avancés pour les tempêtes"""
        st.markdown("### 🌀 Analytics Tempêtes Avancés")
        
        if not self.storm_tracks:
            st.info("Aucune activité cyclonique significative détectée")
            return
        
        # Sélection de la tempête
        storm_names = [storm['name'] for storm in self.storm_tracks]
        selected_storm = st.selectbox("Sélectionner une tempête:", storm_names)
        
        storm_data = next(storm for storm in self.storm_tracks if storm['name'] == selected_storm)
        
        # Cartographie avancée
        col1, col2 = st.columns([3, 1])
        
        with col1:
            fig = go.Figure()
            
            lats = [point['lat'] for point in storm_data['track']]
            lons = [point['lon'] for point in storm_data['track']]
            intensities = [point['intensity'] for point in storm_data['track']]
            pressures = [point['pressure'] for point in storm_data['track']]
            
            # Trajectoire avec intensité
            fig.add_trace(go.Scattermapbox(
                lat=lats,
                lon=lons,
                mode='lines+markers',
                marker=dict(
                    size=10,
                    color=intensities,
                    colorscale='Viridis',
                    colorbar=dict(title="Intensité (km/h)"),
                    showscale=True
                ),
                line=dict(width=4, color='red'),
                text=[f"Vitesse: {intensity:.1f} km/h<br>Pression: {pressure:.1f} hPa" 
                      for intensity, pressure in zip(intensities, pressures)],
                hoverinfo='text'
            ))
            
            fig.update_layout(
                mapbox=dict(
                    style="stamen-terrain",
                    center=dict(lat=np.mean(lats), lon=np.mean(lons)),
                    zoom=3,
                    bearing=0,
                    pitch=0
                ),
                height=500,
                margin=dict(l=0, r=0, t=0, b=0),
                title=f"Trajectoire de {selected_storm}"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Statistiques avancées de la tempête
            current_state = storm_data['track'][-1]
            
            st.markdown("#### 📊 Statistiques")
            st.metric("Intensité Actuelle", f"{current_state['intensity']:.1f} km/h")
            st.metric("Catégorie", current_state['category'])
            st.metric("Pression", f"{current_state['pressure']:.1f} hPa")
            st.metric("Rayon d'Action", f"{current_state['radius']:.0f} km")
            st.metric("Niveau de Menace", storm_data['current_threat'])
            
            # Évolution de l'intensité
            intensity_history = [point['intensity'] for point in storm_data['track']]
            fig_intensity = go.Figure(go.Scatter(
                y=intensity_history,
                mode='lines+markers',
                line=dict(color='red', width=3),
                marker=dict(size=6)
            ))
            fig_intensity.update_layout(
                height=200,
                title="Évolution Intensité",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_intensity, use_container_width=True)
    
    def create_weather_impact_analysis(self):
        """Analyse d'impact météorologique"""
        st.markdown("### 📈 Analyse d'Impact Sectoriel")
        
        # Impacts par secteur
        sectors = {
            "Agriculture": {
                "risk": "Modéré",
                "impact": "Conditions favorables pour les cultures",
                "recommendation": "Poursuivre les activités normales"
            },
            "Transport": {
                "risk": "Élevé", 
                "impact": "Risque de retards aériens et maritimes",
                "recommendation": "Vérifier les horaires avant déplacement"
            },
            "Énergie": {
                "risk": "Faible",
                "impact": "Production solaire et éolienne optimale",
                "recommendation": "Maintenir les niveaux de production"
            },
            "Tourisme": {
                "risk": "Modéré",
                "impact": "Conditions acceptables pour les activités extérieures",
                "recommendation": "Prévoir des solutions de repli"
            }
        }
        
        # Affichage des impacts par secteur
        cols = st.columns(4)
        for idx, (sector, data) in enumerate(sectors.items()):
            with cols[idx]:
                risk_color = {
                    "Élevé": "red",
                    "Modéré": "orange", 
                    "Faible": "green"
                }[data['risk']]
                
                st.markdown(f"""
                <div style='border: 2px solid {risk_color}; border-radius: 12px; padding: 15px; margin: 10px 0;'>
                    <h4 style='margin: 0; color: {risk_color};'>{sector}</h4>
                    <p style='margin: 5px 0;'><strong>Risque:</strong> {data['risk']}</p>
                    <p style='margin: 5px 0;'><strong>Impact:</strong> {data['impact']}</p>
                    <p style='margin: 5px 0;'><strong>Recommandation:</strong> {data['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Graphique d'impact cumulatif
        st.markdown("#### 📊 Impact Économique Potentiel")
        
        impact_data = pd.DataFrame({
            'Secteur': list(sectors.keys()),
            'Impact Potentiel (M€)': np.random.uniform(10, 100, len(sectors)),
            'Probabilité (%)': np.random.uniform(20, 80, len(sectors))
        })
        
        fig = px.scatter(impact_data, x='Probabilité (%)', y='Impact Potentiel (M€)',
                        size='Impact Potentiel (M€)', color='Secteur',
                        hover_name='Secteur', size_max=60,
                        title="Matrice Risque-Impact par Secteur")
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_climate_analytics(self):
        """Analytics climatiques avancés"""
        st.markdown("### 🌍 Analytics Climatiques")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Analyse des tendances long terme
            st.markdown("#### 📈 Tendances Climatiques")
            
            monthly_data = self.weather_data.groupby(
                self.weather_data['datetime'].dt.to_period('M')
            ).agg({
                'temperature': 'mean',
                'precipitation': 'sum',
                'wind_speed': 'mean'
            }).reset_index()
            
            monthly_data['datetime'] = monthly_data['datetime'].astype(str)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(x=monthly_data['datetime'], y=monthly_data['temperature'],
                          name='Température Moyenne', line=dict(color='red', width=3)),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Bar(x=monthly_data['datetime'], y=monthly_data['precipitation'],
                       name='Précipitations', marker_color='blue', opacity=0.6),
                secondary_y=True,
            )
            
            fig.update_layout(
                title="Tendances Mensuelles",
                xaxis_title="Mois",
                height=400
            )
            
            fig.update_yaxes(title_text="Température (°C)", secondary_y=False)
            fig.update_yaxes(title_text="Précipitations (mm)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Indices climatiques
            st.markdown("#### 🔍 Indices Avancés")
            
            current = self.weather_data.iloc[-1]
            
            indices = [
                ("🌡️ Indice de Chaleur", current['heat_index'], "°C", 
                 "✅ Normal" if current['heat_index'] < 30 else "⚠️ Élevé"),
                ("💨 Indice de Vent", current['wind_speed'] / 50, "", 
                 "✅ Faible" if current['wind_speed'] < 30 else "⚠️ Fort"),
                ("🌧️ Indice de Précipitation", current['precipitation'] / 10, "", 
                 "✅ Sec" if current['precipitation'] < 2 else "⚠️ Humide"),
                ("👁️ Indice de Visibilité", current['visibility'] / 20, "", 
                 "✅ Bonne" if current['visibility'] > 10 else "⚠️ Réduite")
            ]
            
            for name, value, unit, status in indices:
                st.metric(name, f"{value:.1f}{unit}", status)
            
            # Radar des conditions
            st.markdown("#### 🎯 Conditions Actuelles")
            categories = ['Température', 'Vent', 'Précipitation', 'Visibilité', 'Humidité']
            values = [current['temperature']/40, current['wind_speed']/50, 
                     current['precipitation']/10, current['visibility']/20, current['humidity']/100]
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                line=dict(color='blue', width=2)
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1])
                ),
                showlegend=False,
                height=300,
                margin=dict(l=50, r=50, t=30, b=30)
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)

def create_enhanced_ventusky_integration():
    """Crée l'intégration Ventusky améliorée avec plus de fonctionnalités"""
    
    enhanced_ventusky_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ventusky Pro+ Intégré</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
                color: white;
            }
            .browser-container {
                width: 100%;
                height: 750px;
                background: #2d2d2d;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 12px 40px rgba(0,0,0,0.4);
                border: 1px solid rgba(255,255,255,0.1);
            }
            .browser-header {
                background: linear-gradient(135deg, #3d3d3d 0%, #4d4d4d 100%);
                padding: 18px 25px;
                display: flex;
                align-items: center;
                gap: 20px;
                border-bottom: 2px solid rgba(255,255,255,0.1);
            }
            .browser-controls {
                display: flex;
                gap: 10px;
            }
            .control-btn {
                width: 14px;
                height: 14px;
                border-radius: 50%;
                cursor: pointer;
                transition: transform 0.2s ease;
            }
            .control-btn:hover {
                transform: scale(1.1);
            }
            .close { background: #ff5f57; }
            .minimize { background: #ffbd2e; }
            .maximize { background: #28ca42; }
            .url-display {
                flex: 1;
                background: rgba(255,255,255,0.1);
                border: 2px solid rgba(255,255,255,0.2);
                border-radius: 25px;
                padding: 12px 25px;
                color: white;
                font-size: 14px;
                margin: 0 25px;
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }
            .url-display:focus {
                border-color: #00aaff;
                box-shadow: 0 0 20px rgba(0,170,255,0.3);
            }
            .browser-actions {
                display: flex;
                gap: 15px;
            }
            .action-btn {
                background: linear-gradient(135deg, #00aaff, #0066cc);
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 12px rgba(0,170,255,0.3);
            }
            .action-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,170,255,0.4);
            }
            .action-btn.secondary {
                background: linear-gradient(135deg, #667eea, #764ba2);
            }
            .quick-layers {
                display: flex;
                gap: 10px;
                margin-left: 20px;
            }
            .layer-btn {
                background: rgba(255,255,255,0.1);
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.3s ease;
            }
            .layer-btn.active {
                background: #00aaff;
                box-shadow: 0 0 15px rgba(0,170,255,0.5);
            }
            .layer-btn:hover {
                background: rgba(255,255,255,0.2);
            }
            .browser-content {
                height: calc(100% - 70px);
                background: white;
                position: relative;
            }
            .ventusky-frame {
                width: 100%;
                height: 100%;
                border: none;
                transition: opacity 0.3s ease;
            }
            .status-bar {
                background: rgba(0,0,0,0.8);
                padding: 10px 25px;
                font-size: 12px;
                color: #ccc;
                border-top: 1px solid rgba(255,255,255,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .connection-status {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .status-indicator {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #28ca42;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            .loading-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                display: none;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .loading-content {
                text-align: center;
                color: white;
            }
            .spinner {
                border: 4px solid rgba(255,255,255,0.3);
                border-top: 4px solid #00aaff;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
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
                
                <div class="quick-layers">
                    <button class="layer-btn active" data-layer="wind">💨 Vent</button>
                    <button class="layer-btn" data-layer="temp">🌡️ Température</button>
                    <button class="layer-btn" data-layer="prec">🌧️ Précipitation</button>
                    <button class="layer-btn" data-layer="press">📊 Pression</button>
                    <button class="layer-btn" data-layer="cloud">☁️ Nuages</button>
                </div>
                
                <div class="url-display" id="urlDisplay">https://www.ventusky.com</div>
                
                <div class="browser-actions">
                    <button class="action-btn" onclick="refreshVentusky()">
                        <span>🔄</span> Actualiser
                    </button>
                    <button class="action-btn" onclick="fullscreenVentusky()">
                        <span>📺</span> Plein Écran
                    </button>
                    <button class="action-btn secondary" onclick="showAnalytics()">
                        <span>📈</span> Analytics
                    </button>
                </div>
            </div>
            
            <div class="browser-content">
                <div class="loading-overlay" id="loadingOverlay">
                    <div class="loading-content">
                        <div class="spinner"></div>
                        <div>Chargement Ventusky...</div>
                    </div>
                </div>
                
                <iframe class="ventusky-frame" id="ventuskyFrame" 
                        src="https://www.ventusky.com"
                        allowfullscreen></iframe>
            </div>
            
            <div class="status-bar">
                <span id="statusText">Ventusky Pro+ - Surveillance météo active</span>
                <div class="connection-status">
                    <div class="status-indicator"></div>
                    <span id="connectionStatus">Connecté</span>
                    <span id="lastUpdate">• Dernière MAJ: <span id="updateTime">--:--:--</span></span>
                </div>
            </div>
        </div>

        <script>
        let currentLayer = 'wind';
        let autoRefreshInterval;
        
        // Configuration des layers Ventusky
        const layerConfig = {
            'wind': '?p=wind',
            'temp': '?p=temp',
            'prec': '?p=prec', 
            'press': '?p=press',
            'cloud': '?p=cloud',
            'snow': '?p=snow',
            'wave': '?p=wave'
        };
        
        function refreshVentusky() {
            showLoading(true);
            const frame = document.getElementById('ventuskyFrame');
            frame.src = frame.src;
            updateStatus('Actualisation en cours...');
            
            setTimeout(() => {
                showLoading(false);
                updateLastUpdate();
                updateStatus('Ventusky actualisé avec succès');
            }, 3000);
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
            showLoading(true);
            currentLayer = layer;
            
            // Mettre à jour les boutons
            document.querySelectorAll('.layer-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Changer la layer
            const baseUrl = 'https://www.ventusky.com';
            const frame = document.getElementById('ventuskyFrame');
            frame.src = baseUrl + layerConfig[layer];
            
            updateStatus(`Layer activée: ${getLayerName(layer)}`);
            
            setTimeout(() => {
                showLoading(false);
            }, 2000);
        }
        
        function getLayerName(layer) {
            const names = {
                'wind': 'Vent',
                'temp': 'Température',
                'prec': 'Précipitation',
                'press': 'Pression',
                'cloud': 'Nuages',
                'snow': 'Neige',
                'wave': 'Vagues'
            };
            return names[layer] || layer;
        }
        
        function showAnalytics() {
            updateStatus('Ouverture des analytics Ventusky...');
            // Ici on pourrait ouvrir un modal avec des analytics supplémentaires
            alert('Fonctionnalité Analytics avancée - En développement');
        }
        
        function showLoading(show) {
            const overlay = document.getElementById('loadingOverlay');
            overlay.style.display = show ? 'flex' : 'none';
        }
        
        function updateStatus(message) {
            document.getElementById('statusText').textContent = message;
        }
        
        function updateLastUpdate() {
            const now = new Date();
            document.getElementById('updateTime').textContent = 
                now.toLocaleTimeString('fr-FR');
        }
        
        function startAutoRefresh() {
            // Actualisation automatique toutes les 10 minutes
            autoRefreshInterval = setInterval(refreshVentusky, 600000);
        }
        
        function stopAutoRefresh() {
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
            }
        }
        
        // Événements
        document.addEventListener('DOMContentLoaded', function() {
            // Configurer les boutons de layer
            document.querySelectorAll('.layer-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const layer = this.getAttribute('data-layer');
                    switchLayer(layer);
                });
            });
            
            // Surveillance de la connexion
            setInterval(() => {
                const frame = document.getElementById('ventuskyFrame');
                try {
                    if (frame.contentWindow && frame.contentWindow.location.href) {
                        document.getElementById('connectionStatus').textContent = 'Connecté';
                        document.querySelector('.status-indicator').style.background = '#28ca42';
                    }
                } catch (e) {
                    document.getElementById('connectionStatus').textContent = 'Chargement...';
                    document.querySelector('.status-indicator').style.background = '#ffbd2e';
                }
            }, 5000);
            
            // Démarrer l'actualisation automatique
            startAutoRefresh();
            updateLastUpdate();
        });
        
        // Raccourcis clavier
        document.addEventListener('keydown', function(event) {
            if (event.ctrlKey || event.metaKey) {
                switch(event.key) {
                    case 'r':
                        event.preventDefault();
                        refreshVentusky();
                        break;
                    case 'f':
                        event.preventDefault();
                        fullscreenVentusky();
                        break;
                }
            }
            
            // Changer de layer avec les chiffres
            if (event.key >= '1' && event.key <= '6') {
                const layers = Object.keys(layerConfig);
                const layerIndex = parseInt(event.key) - 1;
                if (layerIndex < layers.length) {
                    const layer = layers[layerIndex];
                    switchLayer(layer);
                }
            }
        });
        </script>
    </body>
    </html>
    """
    return enhanced_ventusky_html

def main():
    st.markdown('<h1 class="main-header">🌪️ Ventusky Pro+ - Analytics Météo Avancées</h1>', 
                unsafe_allow_html=True)
    
    # Initialisation des analytics avancés
    analytics = EnhancedWeatherAnalytics()
    
    # Sidebar avancée
    with st.sidebar:
        st.markdown("## 🎛️ Centre de Contrôle Pro+")
        
        st.markdown("### 📊 Dashboard Settings")
        analysis_mode = st.selectbox(
            "Mode d'analyse:",
            ["Temps Réel", "Historique", "Prédictif", "Comparatif"],
            index=0
        )
        
        auto_refresh = st.checkbox("🔄 Actualisation Auto", value=True)
        refresh_rate = st.select_slider("Fréquence:", options=[1, 5, 10, 15, 30], value=5)
        
        st.markdown("### ⚠️ System Alerts")
        alert_level = st.radio(
            "Niveau d'alerte:",
            ["Toutes", "Critiques seulement", "Désactivées"],
            index=0
        )
        
        st.markdown("### 🔧 Advanced Features")
        ai_analysis = st.checkbox("🧠 Analyse IA", value=True)
        storm_tracking = st.checkbox("🌀 Suivi Tempêtes", value=True)
        impact_analysis = st.checkbox("📈 Analyse d'Impact", value=True)
        
        st.markdown("---")
        st.markdown("## 📈 Quick Stats")
        
        current_data = analytics.weather_data.iloc[-1]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌡️ Temp", f"{current_data['temperature']:.1f}°C")
            st.metric("💨 Vent", f"{current_data['wind_speed']:.1f} km/h")
        with col2:
            st.metric("📊 Press", f"{current_data['pressure']:.1f} hPa")
            st.metric("💧 Humid", f"{current_data['humidity']:.1f}%")
    
    # Navigation par onglets principale améliorée
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Ventusky Pro+", 
        "🧠 IA Analytics", 
        "🌀 Storm Center",
        "📈 Impact Analysis", 
        "🌍 Climate Analytics"
    ])
    
    with tab1:
        st.markdown("### 💨 Ventusky Pro+ - Interface Avancée")
        
        # Alertes en temps réel
        for alert in analytics.weather_alerts:
            if alert['severity'] == 'Élevée':
                st.markdown(f'<div class="alert-critical">🚨 {alert["title"]} - {alert["region"]}<br>{alert["description"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-warning">⚠️ {alert["title"]} - {alert["region"]}<br>{alert["description"]}</div>', 
                           unsafe_allow_html=True)
        
        # Métriques avancées
        analytics.create_advanced_metrics_dashboard()
        
        # Intégration Ventusky améliorée
        st.markdown("#### 🗺️ Interface Ventusky Pro+")
        ventusky_html = create_enhanced_ventusky_integration()
        html(ventusky_html, height=800, scrolling=False)
        
        # Panel de contrôle rapide
        st.markdown("#### 🎮 Contrôles Rapides")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🔄 Sync Data", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("📊 Export", use_container_width=True):
                st.success("Données exportées avec succès")
        with col3:
            if st.button("📱 Mobile View", use_container_width=True):
                st.info("Vue mobile activée")
        with col4:
            if st.button("⚙️ Settings", use_container_width=True):
                st.info("Paramètres ouverts")
    
    with tab2:
        st.markdown("### 🧠 Intelligence Artificielle Météo")
        analytics.create_ai_weather_analysis()
        
        # Insights supplémentaires
        st.markdown("#### 🔍 Détection d'Anomalies Avancée")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 Modèles de Comportement")
            behaviors = [
                ("Cycle diurne", "Normal", "✅"),
                ("Pression atmosphérique", "Légère baisse", "⚠️"),
                ("Modèles de vent", "Stable", "✅"),
                ("Humidité relative", "Augmentation", "🔍")
            ]
            
            for behavior, status, icon in behaviors:
                st.write(f"{icon} {behavior}: {status}")
        
        with col2:
            st.markdown("##### 🎯 Recommandations IA")
            recommendations = [
                "Surveiller l'évolution de la pression",
                "Prévoir une augmentation des précipitations sous 24h",
                "Conditions favorables pour l'énergie éolienne",
                "Risque de brouillard matinal modéré"
            ]
            
            for rec in recommendations:
                st.write(f"• {rec}")
    
    with tab3:
        st.markdown("### 🌀 Centre de Surveillance des Tempêtes")
        analytics.create_advanced_storm_analytics()
        
        # Alertes tempêtes en temps réel
        st.markdown("#### ⚠️ Alertes Tempêtes Actives")
        for storm in analytics.storm_tracks:
            if storm['current_threat'] == 'Élevé':
                st.markdown(f'<div class="alert-critical">🚨 {storm["name"]} - Menace Élevée<br>Intensité: {storm["track"][-1]["intensity"]:.1f} km/h</div>', 
                           unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📈 Analyse d'Impact Économique")
        analytics.create_weather_impact_analysis()
        
        # Graphique d'impact temporel
        st.markdown("#### 📅 Impact Temporel")
        impact_timeline = pd.DataFrame({
            'Date': pd.date_range(start=datetime.now(), periods=7, freq='D'),
            'Impact Agricole': np.random.uniform(10, 50, 7),
            'Impact Transport': np.random.uniform(20, 80, 7),
            'Impact Énergie': np.random.uniform(5, 30, 7)
        })
        
        fig = px.area(impact_timeline, x='Date', y=['Impact Agricole', 'Impact Transport', 'Impact Énergie'],
                     title="Projection d'Impact sur 7 Jours")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.markdown("### 🌍 Analytics Climatiques Avancés")
        analytics.create_climate_analytics()
        
        # Indices climatiques globaux
        st.markdown("#### 🌡️ Indices Climatiques Globaux")
        indices = [
            ("Indice de Réchauffement", "+1.2°C", "📈"),
            ("Anomalie de Précipitation", "+5%", "🌧️"),
            ("Fréquence des Événements Extrêmes", "+15%", "⚠️"),
            ("Niveau de la Mer", "+3.2 mm/an", "🌊")
        ]
        
        cols = st.columns(4)
        for idx, (name, value, icon) in enumerate(indices):
            with cols[idx]:
                st.metric(f"{icon} {name}", value)
    
    # Actualisation automatique
    if auto_refresh:
        time.sleep(refresh_rate * 60)
        st.rerun()

if __name__ == "__main__":
    main()
