import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(layout="wide", page_title="Quantum Learning Lab")

# ======================
# STYLE
# ======================
# st.markdown("""
# <style>
# section[data-testid="stSidebar"] {
#     background:#0b1220;
# }
# section[data-testid="stSidebar"] label,
# section[data-testid="stSidebar"] h1,
# section[data-testid="stSidebar"] h2,
# section[data-testid="stSidebar"] h3 {
#     color:white !important;
# }
# .stButton>button {
#     background:#06b6d4;
#     color:white;
#     border-radius:8px;
#     font-weight:bold;
# }
# </style>
# """, unsafe_allow_html=True)

st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"] {
    background:#0b1220;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    color:white !important;
}

/* RADIO BUTTON TEXT (MAIN FIX) */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    color:white !important;
    font-weight:500 !important;
}

/* Radio selected text */
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color:white !important;
}

/* Button styling */
.stButton>button {
    background:#06b6d4;
    color:white;
    border-radius:8px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ======================
# SESSION STATE (FIXED)
# ======================
if "state" not in st.session_state:
    st.session_state.state = np.array([1.,0.])

if "progress" not in st.session_state:
    st.session_state.progress = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "circuit" not in st.session_state:
    st.session_state.circuit = []

# ======================
# BASIC GATES
# ======================
H=(1/np.sqrt(2))*np.array([[1,1],[1,-1]])
X=np.array([[0,1],[1,0]])
Y=np.array([[0,-1j],[1j,0]])
Z=np.array([[1,0],[0,-1]])

gates={"H":H,"X":X,"Y":Y,"Z":Z}

# ======================
# SIDEBAR NAVIGATION
# ======================
st.sidebar.title("⚛ Quantum Lab")

page=st.sidebar.radio(
    "Go to",
    [
        "Bloch Simulation",
        "Circuit Designer",
        "Learning Module",
        "Quiz",
        "Noise & Decoherence",
        "Linear Algebra Lab",
        "Multi-Qubit Research",
        "Quantum Algorithms",
        "3D Viewer"
    ]
)

# ======================
# GLOBAL CONTROLS
# ======================
if page in ["Bloch Simulation","Circuit Designer"]:

    st.sidebar.markdown("---")
    st.sidebar.subheader("Simulation Controls")

    noise=st.sidebar.slider("Noise",0.0,1.0,0.1,0.01)
    decay=st.sidebar.slider("Decoherence",0.0,0.2,0.05,0.01)
    steps=st.sidebar.slider("Steps",50,200,120)

# ======================
# BLOCH SIMULATION
# ======================
if page=="Bloch Simulation":

    st.title("🧭 Bloch Sphere Simulation")

    def simulate():
        traj=[]
        s=np.array([1.,0.,0.])
        for _ in range(steps):
            s*=(1-decay)
            s+=np.random.normal(0,noise,3)
            n=np.linalg.norm(s)
            if n>1:
                s/=n
            traj.append(s.copy())
        return np.array(traj)

    traj=simulate()

    u,v=np.mgrid[0:2*np.pi:30j,0:np.pi:15j]
    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)

    fig=go.Figure()
    fig.add_trace(go.Surface(x=x,y=y,z=z,opacity=0.15,showscale=False))
    fig.add_trace(go.Scatter3d(
        x=traj[:,0],y=traj[:,1],z=traj[:,2],
        mode="lines",
        line=dict(color="cyan",width=5)
    ))

    st.plotly_chart(fig,use_container_width=True)

# ======================
# CIRCUIT DESIGNER
# ======================
if page=="Circuit Designer":

    st.title("🧠 Quantum Circuit Designer")

    gate=st.selectbox("Add Gate",["H","X","Y","Z"])

    if st.button("Add Gate"):
        st.session_state.circuit.append(gate)

    st.write("Circuit:", " → ".join(st.session_state.circuit))

    if st.button("Clear Circuit"):
        st.session_state.circuit=[]
        st.session_state.state=np.array([1.,0.])

    state=np.array([1.,0.])
    for g in st.session_state.circuit:
        state=gates[g] @ state

    st.session_state.state=state

    p0=abs(state[0])**2
    p1=abs(state[1])**2

    c1,c2=st.columns(2)
    c1.metric("P(0)",f"{p0:.3f}")
    c2.metric("P(1)",f"{p1:.3f}")

# ======================
# LEARNING MODULE
# ======================
if page=="Learning Module":

    st.title("🎓 Learning Modules")

    lessons={
        "Qubit":"A qubit exists in both 0 and 1 simultaneously.",
        "Superposition":"Multiple states until measured.",
        "Quantum Gates":"Gates rotate quantum states.",
        "Noise":"Noise causes decoherence."
    }

    selected=st.selectbox("Choose Concept",list(lessons.keys()))
    st.info(lessons[selected])

    if st.button("Mark Lesson Complete"):
        if st.session_state.progress < 5:
            st.session_state.progress += 1
        st.success("Progress Updated!")

# ======================
# QUIZ (FIXED SYSTEM)
# ======================
if page=="Quiz":

    st.title("🧠 Quantum Quiz")

    questions=[
        {
            "q":"A qubit differs from a classical bit because it:",
            "opts":[
                "Stores more memory",
                "Can exist in both 0 and 1 simultaneously",
                "Is faster physically",
                "Uses electricity differently"
            ],
            "correct":1,
            "explain":"Qubits can exist in superposition."
        },
        {
            "q":"Superposition means:",
            "opts":[
                "Only 0",
                "Only 1",
                "Multiple states at once",
                "Duplication"
            ],
            "correct":2,
            "explain":"Superposition allows multiple states simultaneously."
        }
    ]

    if st.session_state.q_index >= len(questions):

        st.success(
            f"🎉 Quiz Complete! Final Score: "
            f"{st.session_state.score}/{len(questions)}"
        )

        if st.button("Restart Quiz"):
            st.session_state.q_index=0
            st.session_state.score=0
            st.session_state.answered=False
            st.rerun()

        st.stop()

    q=questions[st.session_state.q_index]

    st.subheader(f"Question {st.session_state.q_index+1}")
    st.write(q["q"])

    selected=st.radio("Choose:",q["opts"])

    if not st.session_state.answered:

        if st.button("Submit Answer"):

            if selected==q["opts"][q["correct"]]:
                st.success("🎉 Correct! Hurray!")
                st.session_state.score += 1
            else:
                st.error("❌ Wrong!")
                st.info(q["explain"])

            st.session_state.answered=True

    else:
        if st.button("Next Question"):
            st.session_state.q_index += 1
            st.session_state.answered=False
            st.rerun()

# ======================
# NOISE & DECOHERENCE
# ======================
if page=="Noise & Decoherence":

    st.title("🔬 Noise & Decoherence")

    state=st.session_state.state
    noise_type=st.selectbox(
        "Noise Type",
        ["Bit Flip","Phase Flip","Depolarizing"]
    )

    p=st.slider("Noise Strength",0.0,1.0,0.1)

    if noise_type=="Bit Flip":
        noisy=(1-p)*state+p*(X@state)
    elif noise_type=="Phase Flip":
        noisy=(1-p)*state+p*(Z@state)
    else:
        noisy=(1-p)*state+p*np.array([1/np.sqrt(2),1/np.sqrt(2)])

    st.write("P(0):",abs(noisy[0])**2)
    st.write("P(1):",abs(noisy[1])**2)

# ======================
# LINEAR ALGEBRA LAB
# ======================
if page=="Linear Algebra Lab":

    st.title("🧮 Linear Algebra Lab")

    matrix=st.selectbox("Select Matrix",["H","X","Y","Z"])
    M=gates[matrix]

    st.write(M)

    vals,_=np.linalg.eig(M)
    st.write("Eigenvalues:",vals)

# ======================
# MULTI-QUBIT RESEARCH
# ======================
if page=="Multi-Qubit Research":

    st.title("🧪 Multi-Qubit Research")

    CNOT=np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,0,1],
        [0,0,1,0]
    ])

    if st.button("Generate Bell State"):
        st.session_state.state2=(1/np.sqrt(2))*np.array([1,0,0,1])

    if "state2" in st.session_state:
        st.write("Probabilities:",np.abs(st.session_state.state2)**2)

        if st.button("Run CNOT"):
            st.session_state.state2=CNOT@st.session_state.state2
            st.write("New State:",st.session_state.state2)

# ======================
# QUANTUM ALGORITHMS
# ======================
if page=="Quantum Algorithms":

    st.title("🧠 Quantum Algorithms")

    algo=st.selectbox(
        "Choose Algorithm",
        ["Deutsch-Jozsa","Grover","Phase Estimation"]
    )

    if algo=="Deutsch-Jozsa":
        st.info("Determines if function is constant or balanced.")
    elif algo=="Grover":
        it=st.slider("Iterations",1,5,1)
        st.write("Amplification after",it,"iterations.")
    else:
        st.info("Estimates eigenphase of a unitary operator.")

# ======================
# 3D VIEWER
# ======================
if page=="3D Viewer":

    st.title("🌐 3D Bloch Viewer")

    state=st.session_state.state
    theta=2*np.arccos(abs(state[0]))
    phi=np.angle(state[1])

    x=np.sin(theta)*np.cos(phi)
    y=np.sin(theta)*np.sin(phi)
    z=np.cos(theta)

    fig=go.Figure()
    fig.add_trace(go.Scatter3d(
        x=[0,x],y=[0,y],z=[0,z],
        mode='lines+markers'
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-1,1]),
            yaxis=dict(range=[-1,1]),
            zaxis=dict(range=[-1,1])
        ),
        margin=dict(l=0,r=0,b=0,t=0)
    )

    st.plotly_chart(fig,use_container_width=True)

# ======================
# SIDEBAR DASHBOARD
# ======================
st.sidebar.markdown("---")
st.sidebar.subheader("Progress Dashboard")

progress=min(st.session_state.progress*20,100)
st.sidebar.progress(progress/100)
st.sidebar.metric("Progress %",progress)
st.sidebar.metric("Quiz Score",st.session_state.score)
