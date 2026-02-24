import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Quantum Learning Lab")

# =====================
# STYLE
# =====================
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background:#0b1220;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color:white !important;
}
section[data-testid="stSidebar"] button {
    background:#f0f2f6 !important;
    color:black !important;
}
div[data-testid="metric-container"]{
    background:#111827;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# =====================
# STATES
# =====================
if "state" not in st.session_state:
    st.session_state.state=np.array([1.,0.,0.])

if "score" not in st.session_state:
    st.session_state.score=0

if "progress" not in st.session_state:
    st.session_state.progress=0

# =====================
# TITLE
# =====================
st.title("⚛️ Quantum Computing Interactive Learning Lab")
st.caption("Live Quantum Simulation + Learning Platform")

# =====================
# SIDEBAR
# =====================
st.sidebar.title("Simulation Controls")

noise=st.sidebar.slider("Noise",0.0,1.0,0.1,0.01)
decay=st.sidebar.slider("Decoherence",0.0,0.2,0.05,0.01)
steps=st.sidebar.slider("Steps",50,200,120)

mode=st.sidebar.selectbox(
"Simulation Mode",
["Single Qubit","Entanglement","Noise Comparison"]
)

# =====================
# GATES
# =====================
st.sidebar.subheader("Quantum Gates")

if st.sidebar.button("Apply X"):
    st.session_state.state[0]*=-1
if st.sidebar.button("Apply Y"):
    st.session_state.state[1]*=-1
if st.sidebar.button("Apply Z"):
    st.session_state.state[2]*=-1
if st.sidebar.button("Reset"):
    st.session_state.state=np.array([1.,0.,0.])

# =====================
# SIMULATION ENGINE
# =====================
def simulate(noise_level):
    traj=[]
    s=st.session_state.state.copy()

    for _ in range(steps):
        s*= (1-decay)
        s += np.random.normal(0,noise_level,3)

        n=np.linalg.norm(s)
        if n>1:
            s/=n

        traj.append(s.copy())

    return np.array(traj)

# =====================
# BLOCH ANIMATION
# =====================
def bloch_animated(traj):

    u,v=np.mgrid[0:2*np.pi:30j,0:np.pi:15j]
    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)

    sphere=go.Surface(
        x=x,y=y,z=z,
        opacity=0.15,
        colorscale="Blues",
        showscale=False
    )

    path=go.Scatter3d(
        x=traj[:,0],
        y=traj[:,1],
        z=traj[:,2],
        mode="lines",
        line=dict(width=5,color="cyan")
    )

    frames=[]

    for angle in np.linspace(0,2*np.pi,60):
        frames.append(
            go.Frame(
                layout=dict(
                    scene_camera=dict(
                        eye=dict(
                            x=np.cos(angle)*2,
                            y=np.sin(angle)*2,
                            z=1.2
                        )
                    )
                )
            )
        )

    fig=go.Figure(
        data=[sphere,path],
        frames=frames
    )

    fig.update_layout(
        height=600,
        margin=dict(l=0,r=0,b=0,t=0),
        updatemenus=[{
            "type":"buttons",
            "buttons":[
                {
                    "label":"▶ Play Rotation",
                    "method":"animate",
                    "args":[None,{
                        "frame":{"duration":30,"redraw":True},
                        "fromcurrent":True
                    }]
                }
            ]
        }]
    )

    return fig

# =====================
# MAIN DISPLAY (FIXED)
# =====================
traj=simulate(noise)

st.plotly_chart(
    bloch_animated(traj),
    use_container_width=True
)

# =====================
# MEASUREMENT
# =====================
p0=(1+traj[-1,2])/2
p1=1-p0

st.subheader("Measurement Probability")

a,b=st.columns(2)
a.metric("P(0)",f"{p0:.2f}")
b.metric("P(1)",f"{p1:.2f}")

# =====================
# ADVANCED LEARNING PANEL
# =====================
st.markdown("---")
st.header("🎓 Learning Modules")

lessons={
"Qubit":"Qubits exist in continuous quantum state space.",
"Superposition":"Qubits can exist in multiple states at once.",
"Gates":"Quantum gates rotate states on Bloch sphere.",
"Noise":"Noise destroys coherence."
}

selected=st.selectbox("Choose Concept",list(lessons.keys()))
st.info(lessons[selected])

if st.button("Mark Lesson Complete"):
    st.session_state.progress+=1

# =====================
# ADVANCED QUIZ
# =====================
st.markdown("---")
st.header("🧠 Advanced Quiz")

quiz_questions=[
("A qubit differs from a bit because:",
 ["It is physical","It can exist between 0 and 1","It stores more data"],1),

("Superposition means:",
 ["Multiple states","Only 0","Only 1"],0),

("Bloch sphere represents:",
 ["State space","Hardware","Signal"],0),

("Noise causes:",
 ["Collapse","Stability","Speed"],0),

("Decoherence leads to:",
 ["Quantum randomness","Perfect computation","Memory increase"],0),

("Entanglement means:",
 ["Independent states","Linked quantum behavior","Noise"],1)
]

correct_answers=0

for i,(q,opts,corr) in enumerate(quiz_questions):
    ans=st.radio(q,opts,key=f"quiz{i}")
    if ans==opts[corr]:
        correct_answers+=1

if st.button("Submit Full Quiz"):
    st.session_state.score=correct_answers

    st.success(f"Final Score: {correct_answers}/6")

    if correct_answers<=2:
        st.warning("Level: Beginner")
    elif correct_answers<=4:
        st.info("Level: Intermediate")
    else:
        st.success("Level: Quantum Explorer 🚀")

# =====================
# DASHBOARD
# =====================
st.sidebar.markdown("---")
st.sidebar.subheader("Progress Dashboard")

progress=min(st.session_state.progress*20,100)

st.sidebar.progress(progress/100)
st.sidebar.metric("Progress %",progress)
st.sidebar.metric("Quiz Score",st.session_state.score)
