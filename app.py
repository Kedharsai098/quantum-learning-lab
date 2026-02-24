import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(layout="wide", page_title="Quantum Learning Lab")

# ======================
# STYLE (SIDEBAR FIX)
# ======================
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background:#0b1220;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    color:white !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label,
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color:white !important;
}
.stButton>button {
    background:#06b6d4;
    color:white;
    border-radius:8px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ======================
# SESSION STATE
# ======================
if "state" not in st.session_state:
    st.session_state.state=np.array([1.,0.])

if "progress" not in st.session_state:
    st.session_state.progress=0

if "score" not in st.session_state:
    st.session_state.score=0

if "q_index" not in st.session_state:
    st.session_state.q_index=0

if "answered" not in st.session_state:
    st.session_state.answered=False

if "circuit" not in st.session_state:
    st.session_state.circuit=[]

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
    ["Bloch Simulation","Circuit Designer",
     "Learning Module","Quiz",
     "Noise & Decoherence",
     "Linear Algebra Lab",
     "Multi-Qubit Research",
     "Quantum Algorithms",
     "3D Viewer"]
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
            if n>1: s/=n
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
        mode="lines",line=dict(color="cyan",width=5)
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

    st.metric("P(0)",f"{abs(state[0])**2:.3f}")
    st.metric("P(1)",f"{abs(state[1])**2:.3f}")

# ======================
# LEARNING MODULE (UPDATED CONTENT)
# ======================
if page=="Learning Module":

    st.title("🎓 Learning Modules")

    lessons={
        "Qubit":"""A qubit (quantum bit) is the smallest unit of information.

|ψ⟩ = α|0⟩ + β|1⟩

• Classical bit → 0 OR 1  
• Qubit → 0 AND 1 (superposition)  
• Measurement collapses state

💡 Analogy: Spinning coin.""",

        "Superposition":"""Superposition means a qubit can exist in multiple states simultaneously.

1 qubit → 2 states  
2 qubits → 4 states  
3 qubits → 8 states

💡 Enables quantum parallelism.""",

        "Quantum Gates":"""Quantum gates change qubit states.

X → flip  
Y → rotation  
Z → phase change  
H → creates superposition  
CNOT → entanglement

• Gates are reversible  
• Represented as matrices""",

        "Noise & Decoherence":"""Noise introduces errors.

Decoherence = loss of quantum properties.

• Quantum states are fragile  
• Error correction is essential

💡 Analogy: spinning top falling."""
    }

    selected=st.selectbox("Choose Concept",list(lessons.keys()))
    st.info(lessons[selected])

    if st.button("Mark Lesson Complete"):
        if st.session_state.progress < 5:
            st.session_state.progress += 1
        st.success("Progress Updated!")

# ======================
# QUIZ (FULL UPDATED)
# ======================
if page=="Quiz":

    st.title("🧠 Quantum Quiz")

    questions=[
        {"q":"A qubit differs from a classical bit because it:",
         "opts":["Stores more memory","Can exist in both 0 and 1 states simultaneously","Is faster physically","Uses electricity differently"],
         "correct":1,"explain":"Qubits exist in superposition."},

        {"q":"What happens when a qubit is measured?",
         "opts":["It splits","It collapses to 0 or 1","It disappears","Nothing changes"],
         "correct":1,"explain":"Measurement collapses the state."},

        {"q":"Superposition means:",
         "opts":["Only 0","Only 1","Multiple states at once","Duplicated"],
         "correct":2,"explain":"A qubit can exist in multiple states."},

        {"q":"Why is superposition useful?",
         "opts":["Cheaper hardware","Parallel computation","Smaller circuits","Less electricity"],
         "correct":1,"explain":"Quantum parallelism enables huge computation."},

        {"q":"X gate is similar to:",
         "opts":["AND","OR","NOT (flip)","XOR"],
         "correct":2,"explain":"X flips |0⟩ and |1⟩."},

        {"q":"Gate used to create superposition:",
         "opts":["Z","Hadamard","CNOT","Y"],
         "correct":1,"explain":"Hadamard creates equal superposition."},

        {"q":"Quantum gates are:",
         "opts":["Irreversible","Random","Reversible","Destructive"],
         "correct":2,"explain":"Quantum operations are unitary."},

        {"q":"Noise causes:",
         "opts":["Faster execution","Loss of coherence","Better accuracy","Less energy"],
         "correct":1,"explain":"Noise introduces errors."},

        {"q":"Decoherence means:",
         "opts":["Creating qubits","Loss of quantum properties","More superposition","Faster gates"],
         "correct":1,"explain":"Decoherence destroys quantum behavior."}
    ]

    if st.session_state.q_index >= len(questions):
        st.success(f"🎉 Quiz Complete! Score: {st.session_state.score}/{len(questions)}")
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
# SIDEBAR DASHBOARD
# ======================
st.sidebar.markdown("---")
st.sidebar.subheader("Progress Dashboard")

progress=min(st.session_state.progress*20,100)
st.sidebar.progress(progress/100)
st.sidebar.metric("Progress %",progress)
st.sidebar.metric("Quiz Score",st.session_state.score)
