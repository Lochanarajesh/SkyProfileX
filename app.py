import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SkyProfile X",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: #f5f7fb;
}

/* Remove default top padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #101828;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Header */
.hero {
    background: linear-gradient(135deg, #0f172a, #172554);
    padding: 30px 35px;
    border-radius: 24px;
    margin-bottom: 25px;
    color: white;
    box-shadow: 0 10px 30px rgba(15,23,42,0.15);
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 15px;
    color: #cbd5e1;
}

.live {
    display: inline-block;
    background: rgba(34,197,94,0.15);
    color: #4ade80;
    padding: 7px 13px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 15px;
}

/* KPI cards */
.kpi {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px;
    min-height: 135px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.05);
}

.kpi-icon {
    font-size: 25px;
}

.kpi-title {
    color: #64748b;
    font-size: 13px;
    margin-top: 8px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 4px;
}

/* Section title */
.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* Cards */
.info-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 23px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.04);
    height: 100%;
}

.insight-card {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    border: 1px solid #c7d2fe;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 15px;
}

.insight-title {
    font-size: 18px;
    font-weight: 800;
    color: #312e81;
}

.insight-text {
    color: #475569;
    line-height: 1.6;
}

/* Persona */
.persona {
    background: linear-gradient(135deg, #111827, #1e3a8a);
    color: white;
    border-radius: 24px;
    padding: 28px;
    min-height: 310px;
}

.persona-name {
    font-size: 25px;
    font-weight: 800;
}

.persona-sub {
    color: #cbd5e1;
    margin-top: 5px;
}

/* Boarding pass */
.boarding {
    background: white;
    border-radius: 25px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    box-shadow: 0 15px 35px rgba(15,23,42,0.10);
}

.boarding-header {
    background: linear-gradient(135deg, #1d4ed8, #4f46e5);
    padding: 25px;
    color: white;
}

.boarding-body {
    padding: 25px;
}

.flight-route {
    font-size: 34px;
    font-weight: 800;
    color: #0f172a;
}

.detail-label {
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
}

.detail-value {
    font-size: 17px;
    font-weight: 700;
    color: #0f172a;
}

/* Profile tags */
.tag {
    display: inline-block;
    background: #eef2ff;
    color: #3730a3;
    padding: 7px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 12px;
    font-weight: 600;
}

/* Footer */
.footer {
    text-align: center;
    color: #94a3b8;
    padding: 30px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    data = pd.read_csv("airline_passenger_satisfaction.csv")
    data.columns = data.columns.str.strip()
    return data


df = load_data()


# =========================================================
# COLUMN DETECTION
# =========================================================
def get_column(name):
    for col in df.columns:
        if col.lower().strip() == name.lower().strip():
            return col
    return None


id_col = get_column("ID")
class_col = get_column("Class")
customer_col = get_column("Customer Type")
age_col = get_column("Age")
travel_col = get_column("Type of Travel")
distance_col = get_column("Flight Distance")
satisfaction_col = get_column("Satisfaction")
gender_col = get_column("Gender")


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:15px 0 25px 0;">
        <div style="font-size:38px;">✈️</div>
        <div style="font-size:22px;font-weight:800;">SKYPROFILE X</div>
        <div style="font-size:11px;color:#94a3b8;">
            Passenger Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎛️ Filters")

    class_options = df[class_col].dropna().unique().tolist()
    selected_class = st.multiselect(
        "Travel Class",
        class_options,
        default=class_options
    )

    customer_options = df[customer_col].dropna().unique().tolist()
    selected_customer = st.multiselect(
        "Customer Type",
        customer_options,
        default=customer_options
    )

    if travel_col:
        travel_options = df[travel_col].dropna().unique().tolist()

        selected_travel = st.multiselect(
            "Travel Purpose",
            travel_options,
            default=travel_options
        )
    else:
        selected_travel = []

    st.markdown("---")

    st.markdown("""
    <div style="
        background:rgba(255,255,255,0.07);
        padding:15px;
        border-radius:15px;
    ">
    <div style="font-size:12px;color:#94a3b8;">SYSTEM STATUS</div>
    <div style="font-size:15px;font-weight:700;margin-top:5px;">
    🟢 Data Connected
    </div>
    <div style="font-size:11px;color:#94a3b8;margin-top:5px;">
    Passenger intelligence engine ready
    </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# APPLY FILTERS
# =========================================================
filtered = df[
    (df[class_col].isin(selected_class)) &
    (df[customer_col].isin(selected_customer))
]

if travel_col and selected_travel:
    filtered = filtered[
        filtered[travel_col].isin(selected_travel)
    ]

if len(filtered) == 0:
    st.warning("No passengers match the selected filters.")
    st.stop()


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">

<div class="hero-title">
✈️ SKYPROFILE X
</div>

<div class="hero-subtitle">
AI-inspired Passenger Intelligence Platform
</div>

<div class="live">
● LIVE DATA ANALYSIS
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# NAVIGATION
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Command Center",
    "🧬 Passenger DNA",
    "👥 Smart Segmentation",
    "🤖 AI Insights",
    "🎫 Passenger Profile"
])


# =========================================================
# COMMAND CENTER
# =========================================================
with tab1:

    st.markdown(
        '<div class="section-title">📊 Passenger Command Center</div>',
        unsafe_allow_html=True
    )

    total = len(filtered)
    avg_age = filtered[age_col].mean()
    avg_distance = filtered[distance_col].mean()

    if satisfaction_col:
        satisfied = (
            filtered[satisfaction_col]
            .astype(str)
            .str.lower()
            .eq("satisfied")
            .mean() * 100
        )
    else:
        satisfied = 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi">
        <div class="kpi-icon">👥</div>
        <div class="kpi-title">TOTAL PASSENGERS</div>
        <div class="kpi-value">{total:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi">
        <div class="kpi-icon">🎂</div>
        <div class="kpi-title">AVERAGE AGE</div>
        <div class="kpi-value">{avg_age:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi">
        <div class="kpi-icon">🌍</div>
        <div class="kpi-title">AVG FLIGHT DISTANCE</div>
        <div class="kpi-value">{avg_distance:,.0f} km</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-title">SATISFACTION RATE</div>
        <div class="kpi-value">{satisfied:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts
    st.markdown(
        '<div class="section-title">Passenger Behavior</div>',
        unsafe_allow_html=True
    )

    chart1, chart2 = st.columns(2)

    with chart1:

        class_count = (
            filtered[class_col]
            .value_counts()
            .reset_index()
        )

        class_count.columns = ["Class", "Passengers"]

        fig = px.bar(
            class_count,
            x="Class",
            y="Passengers",
            color="Class",
            title="Passengers by Travel Class",
            template="plotly_white"
        )

        fig.update_layout(
            showlegend=False,
            height=360
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart2:

        if satisfaction_col:

            sat_count = (
                filtered[satisfaction_col]
                .value_counts()
                .reset_index()
            )

            sat_count.columns = ["Satisfaction", "Passengers"]

            fig = px.pie(
                sat_count,
                names="Satisfaction",
                values="Passengers",
                hole=0.55,
                title="Passenger Satisfaction"
            )

            fig.update_layout(height=360)

            st.plotly_chart(fig, use_container_width=True)

    # Age vs distance
    st.markdown(
        '<div class="section-title">🔎 Passenger Behavior Map</div>',
        unsafe_allow_html=True
    )

    fig = px.scatter(
        filtered,
        x=age_col,
        y=distance_col,
        color=class_col,
        hover_data=[
            customer_col,
            travel_col
        ] if travel_col else [customer_col],
        title="Age vs Flight Distance",
        template="plotly_white"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# PASSENGER DNA
# =========================================================
with tab2:

    st.markdown(
        '<div class="section-title">🧬 Passenger DNA</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Understand a passenger through their travel behavior, "
        "customer relationship and journey characteristics."
    )

    passenger_id = st.selectbox(
        "Select Passenger",
        filtered[id_col].tolist(),
        key="dna_passenger"
    )

    passenger = filtered[
        filtered[id_col] == passenger_id
    ].iloc[0]

    # Determine persona
    passenger_class = str(passenger[class_col])
    passenger_customer = str(passenger[customer_col])

    if travel_col:
        passenger_travel = str(passenger[travel_col])
    else:
        passenger_travel = "Unknown"

    if passenger_travel.lower() == "business travel":
        persona = "💼 Business Traveler"
        persona_desc = "Primarily associated with business-oriented travel."
    elif passenger_travel.lower() == "personal travel":
        persona = "🌴 Leisure Explorer"
        persona_desc = "Primarily associated with personal or leisure travel."
    else:
        persona = "✈️ Journey Explorer"
        persona_desc = "Passenger profile based on available travel behavior."

    if passenger_customer.lower() == "returning customer":
        loyalty = "High"
    else:
        loyalty = "New / Developing"

    p1, p2 = st.columns([1, 1.5])

    with p1:

        st.markdown(f"""
        <div class="persona">

        <div style="font-size:45px;">🧬</div>

        <div class="persona-name">
        {persona}
        </div>

        <div class="persona-sub">
        {persona_desc}
        </div>

        <br>

        <div>
        <span class="tag">{passenger_class}</span>
        <span class="tag">{passenger_customer}</span>
        <span class="tag">{passenger_travel}</span>
        </div>

        <br>

        <b>Relationship:</b> {loyalty}

        </div>
        """, unsafe_allow_html=True)

    with p2:

        st.markdown(
            '<div class="info-card"><h3>🔍 Profile Signals</h3>',
            unsafe_allow_html=True
        )

        st.write(
            f"**Age:** {passenger[age_col]} years"
        )

        st.write(
            f"**Travel Class:** {passenger[class_col]}"
        )

        st.write(
            f"**Flight Distance:** {passenger[distance_col]} km"
        )

        st.write(
            f"**Customer Type:** {passenger[customer_col]}"
        )

        if travel_col:
            st.write(
                f"**Travel Purpose:** {passenger[travel_col]}"
            )

        if satisfaction_col:
            st.write(
                f"**Satisfaction:** {passenger[satisfaction_col]}"
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # WHY section
    st.markdown(
        '<div class="section-title">🤖 Why does this profile look like this?</div>',
        unsafe_allow_html=True
    )

    reasons = []

    if passenger_customer.lower() == "returning customer":
        reasons.append("✓ Returning customer relationship")
    else:
        reasons.append("✓ First-time customer")

    reasons.append(
        f"✓ Travels in {passenger_class} class"
    )

    if travel_col:
        reasons.append(
            f"✓ Travel purpose: {passenger_travel}"
        )

    if passenger[distance_col] >= filtered[distance_col].median():
        reasons.append(
            "✓ Flight distance is above the filtered passenger median"
        )
    else:
        reasons.append(
            "✓ Flight distance is below the filtered passenger median"
        )

    st.markdown(
        '<div class="insight-card">'
        '<div class="insight-title">Profile Explanation</div>'
        '<div class="insight-text">'
        + "<br>".join(reasons)
        + '</div></div>',
        unsafe_allow_html=True
    )


# =========================================================
# SMART SEGMENTATION
# =========================================================
with tab3:

    st.markdown(
        '<div class="section-title">👥 Smart Passenger Segmentation</div>',
        unsafe_allow_html=True
    )

    # Create meaningful segments using existing fields
    def create_segment(row):

        travel = str(row[travel_col]).lower() if travel_col else ""
        customer = str(row[customer_col]).lower()
        cls = str(row[class_col]).lower()

        if "business" in travel and "returning" in customer:
            return "💼 Loyal Business"

        elif "business" in travel:
            return "🧳 Business Traveler"

        elif "personal" in travel and "returning" in customer:
            return "🔄 Returning Leisure"

        elif "personal" in travel:
            return "🌴 Leisure Explorer"

        elif "business" in cls:
            return "⭐ Premium Traveler"

        else:
            return "✈️ General Traveler"

    segmented = filtered.copy()

    if travel_col:
        segmented["Passenger Segment"] = segmented.apply(
            create_segment,
            axis=1
        )
    else:
        segmented["Passenger Segment"] = segmented.apply(
            create_segment,
            axis=1
        )

    segment_counts = (
        segmented["Passenger Segment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "Segment",
        "Passengers"
    ]

    left, right = st.columns([1, 1])

    with left:

        fig = px.pie(
            segment_counts,
            names="Segment",
            values="Passengers",
            hole=0.55,
            title="Passenger Segment Distribution"
        )

        fig.update_layout(height=430)

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig = px.bar(
            segment_counts,
            x="Passengers",
            y="Segment",
            orientation="h",
            title="Passenger Segments",
            template="plotly_white"
        )

        fig.update_layout(height=430)

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title">🎯 Segment Intelligence</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(min(3, len(segment_counts)))

    for i, row in segment_counts.head(3).iterrows():

        with cols[i % 3]:

            st.markdown(f"""
            <div class="info-card">

            <div style="font-size:30px;">
            {row['Segment'].split()[0]}
            </div>

            <h3>{' '.join(row['Segment'].split()[1:])}</h3>

            <div style="
                font-size:28px;
                font-weight:800;
                color:#1d4ed8;
            ">
            {row['Passengers']:,}
            </div>

            <div style="color:#64748b;">
            passengers
            </div>

            </div>
            """, unsafe_allow_html=True)


# =========================================================
# AI INSIGHTS
# =========================================================
with tab4:

    st.markdown(
        '<div class="section-title">🤖 SKY AI — Passenger Intelligence</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Automated insights generated from the currently filtered passenger data."
    )

    most_class = filtered[class_col].mode()[0]
    most_customer = filtered[customer_col].mode()[0]

    if travel_col:
        most_travel = filtered[travel_col].mode()[0]
    else:
        most_travel = "N/A"

    longest_distance = filtered[distance_col].max()

    insights = [
        (
            "🎯 Dominant Passenger Group",
            f"The most common travel class in the current selection is "
            f"**{most_class}**."
        ),

        (
            "🔄 Customer Relationship",
            f"The dominant customer type is **{most_customer}**."
        ),

        (
            "✈️ Travel Purpose",
            f"The most common travel purpose is **{most_travel}**."
        ),

        (
            "🌍 Journey Pattern",
            f"The longest recorded flight distance in this selection is "
            f"**{longest_distance:,.0f} km**."
        )
    ]

    for title, text in insights:

        st.markdown(f"""
        <div class="insight-card">

        <div class="insight-title">
        {title}
        </div>

        <div class="insight-text">
        {text}
        </div>

        </div>
        """, unsafe_allow_html=True)

    # Satisfaction by class
    if satisfaction_col:

        st.markdown(
            '<div class="section-title">📈 Satisfaction by Class</div>',
            unsafe_allow_html=True
        )

        satisfaction_class = (
            filtered
            .groupby(class_col)[satisfaction_col]
            .apply(
                lambda x: (
                    x.astype(str)
                    .str.lower()
                    .eq("satisfied")
                    .mean() * 100
                )
            )
            .reset_index(name="Satisfaction Rate")
        )

        fig = px.bar(
            satisfaction_class,
            x=class_col,
            y="Satisfaction Rate",
            text="Satisfaction Rate",
            title="Satisfaction Rate by Travel Class",
            template="plotly_white"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_layout(
            yaxis_title="Satisfied Passengers (%)",
            height=420
        )

        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "💡 Note: These are data-driven insights, not predictions from a trained machine-learning model. "
        "A real prediction engine can be added later."
    )


# =========================================================
# PASSENGER PROFILE / BOARDING PASS
# =========================================================

with tab5:

    st.markdown(
        '<div class="section-title">🎫 Passenger Profile</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Select a passenger to view their complete travel profile."
    )

    # Select passenger
    selected_id = st.selectbox(
        "Select Passenger ID",
        filtered[id_col].tolist(),
        key="profile_passenger"
    )

    # Get selected passenger
    p = filtered[
        filtered[id_col] == selected_id
    ].iloc[0]

    # Travel purpose
    if travel_col:
        travel_value = p[travel_col]
    else:
        travel_value = "N/A"

    # Satisfaction
    if satisfaction_col:
        satisfaction_value = p[satisfaction_col]
    else:
        satisfaction_value = "N/A"

    # Generate profile button
    generate_profile = st.button(
        "✨ Generate Passenger Profile",
        use_container_width=False
    )

    # Show profile after clicking
    if generate_profile:

        st.markdown(
            "\n".join(line.strip() for line in """
            <div style="
                margin-top:25px;
                margin-bottom:15px;
                font-size:20px;
                font-weight:700;
                color:#0f172a;
            ">
                ✨ Passenger Intelligence Profile
            </div>
            """.split("\n")),
            unsafe_allow_html=True
        )

        st.markdown(
            "\n".join(line.strip() for line in f"""
            <div class="boarding">

                <!-- HEADER -->
                <div class="boarding-header">

                    <div style="
                        font-size:14px;
                        opacity:0.85;
                        letter-spacing:1px;
                    ">
                        SKYPROFILE X
                    </div>

                    <div style="
                        font-size:26px;
                        font-weight:800;
                        margin-top:8px;
                    ">
                        ✈️ PASSENGER PROFILE
                    </div>

                </div>

                <!-- BODY -->
                <div class="boarding-body">

                    <div class="flight-route">
                        {p[class_col]}
                    </div>

                    <div style="
                        color:#64748b;
                        margin-bottom:25px;
                    ">
                        Passenger ID: <b>{p[id_col]}</b>
                    </div>

                    <!-- DETAILS -->
                    <div style="
                        display:grid;
                        grid-template-columns:repeat(2,1fr);
                        gap:25px;
                    ">

                        <div>
                            <div class="detail-label">
                                Customer Type
                            </div>

                            <div class="detail-value">
                                {p[customer_col]}
                            </div>
                        </div>


                        <div>
                            <div class="detail-label">
                                Travel Purpose
                            </div>

                            <div class="detail-value">
                                {travel_value}
                            </div>
                        </div>


                        <div>
                            <div class="detail-label">
                                Age
                            </div>

                            <div class="detail-value">
                                {p[age_col]} years
                            </div>
                        </div>


                        <div>
                            <div class="detail-label">
                                Flight Distance
                            </div>

                            <div class="detail-value">
                                {p[distance_col]} km
                            </div>
                        </div>


                        <div>
                            <div class="detail-label">
                                Satisfaction
                            </div>

                            <div class="detail-value">
                                {satisfaction_value}
                            </div>
                        </div>


                        <div>
                            <div class="detail-label">
                                Travel Class
                            </div>

                            <div class="detail-value">
                                {p[class_col]}
                            </div>
                        </div>

                    </div>

                    <hr style="margin:30px 0;">

                    <!-- PROFILE SUMMARY -->
                    <div style="
                        background:#eef2ff;
                        padding:20px;
                        border-radius:15px;
                    ">

                        <div style="
                            font-weight:800;
                            color:#3730a3;
                            font-size:16px;
                        ">
                            🧬 PROFILE SUMMARY
                        </div>

                        <div style="
                            margin-top:10px;
                            color:#475569;
                            line-height:1.7;
                        ">

                            This passenger is a
                            <b>{p[customer_col]}</b>
                            customer travelling in
                            <b>{p[class_col]}</b> class
                            for <b>{travel_value}</b>.

                            The passenger is
                            <b>{p[age_col]} years old</b>
                            and has travelled approximately
                            <b>{p[distance_col]} km</b>.

                            Recorded satisfaction:
                            <b>{satisfaction_value}</b>.

                        </div>

                    </div>

                </div>

            </div>
            """.split("\n")),
            unsafe_allow_html=True
        )