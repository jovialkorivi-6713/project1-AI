
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Data Analysis",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🎓 Student Data Analysis Dashboard")

st.write(
    "Upload a student CSV file to analyze marks, attendance, "
    "grades, departments and student performance."
)

st.markdown("---")


# =========================================================
# FILE UPLOAD
# =========================================================

st.sidebar.header("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload Student CSV File",
    type=["csv"],
    help="Upload a CSV containing student information."
)


# Stop application until file is uploaded

if uploaded_file is None:

    st.info(
        "👆 Please upload your student CSV file using "
        "the uploader in the sidebar."
    )

    st.markdown("""
    ### Required Columns

    Your CSV should contain these columns:

    - Roll_No
    - Name
    - Gender
    - Age
    - Marks
    - Attendance
    - Department
    - Grade

    **Note:** `Attendence` is also accepted.
    """)

    st.stop()


# =========================================================
# READ CSV
# =========================================================

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error(
        f"❌ Unable to read the CSV file.\n\nError: {e}"
    )

    st.stop()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)


# =========================================================
# HANDLE COMMON COLUMN NAME VARIATIONS
# =========================================================

column_mapping = {

    "rollno": "roll_no",

    "roll_number": "roll_no",

    "roll_no": "roll_no",

    "attendance": "attendance",

    "attendence": "attendance",

    "marks": "marks",

    "name": "name",

    "gender": "gender",

    "age": "age",

    "department": "department",

    "grade": "grade"
}


df.rename(
    columns={
        column: column_mapping.get(column, column)
        for column in df.columns
    },
    inplace=True
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [

    "roll_no",
    "name",
    "gender",
    "age",
    "marks",
    "attendance",
    "department",
    "grade"

]


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

missing_columns = [

    column

    for column in required_columns

    if column not in df.columns

]


if missing_columns:

    st.error(
        "❌ Your CSV is missing the following required columns:"
    )

    for column in missing_columns:

        st.write(f"• `{column}`")

    st.info("""
    ### Expected columns

    `Roll_No, Name, Gender, Age, Marks, Attendance, Department, Grade`

    If your column is named `Attendence`, that is also supported.
    """)

    st.stop()


# =========================================================
# CONVERT NUMERIC COLUMNS
# =========================================================

df["age"] = pd.to_numeric(
    df["age"],
    errors="coerce"
)

df["marks"] = pd.to_numeric(
    df["marks"],
    errors="coerce"
)

df["attendance"] = pd.to_numeric(
    df["attendance"],
    errors="coerce"
)


# =========================================================
# REMOVE COMPLETELY EMPTY ROWS
# =========================================================

df = df.dropna(
    how="all"
).reset_index(drop=True)


# =========================================================
# SUCCESS MESSAGE
# =========================================================

st.success(
    f"✅ Dataset uploaded successfully! "
    f"Total records: {len(df)}"
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("---")

st.sidebar.header("🔎 Filters")


# Department filter

department_list = sorted(
    df["department"]
    .dropna()
    .astype(str)
    .unique()
)


selected_departments = st.sidebar.multiselect(

    "Department",

    department_list,

    default=department_list

)


# Gender filter

gender_list = sorted(
    df["gender"]
    .dropna()
    .astype(str)
    .unique()
)


selected_genders = st.sidebar.multiselect(

    "Gender",

    gender_list,

    default=gender_list

)


# Grade filter

grade_list = sorted(
    df["grade"]
    .dropna()
    .astype(str)
    .unique()
)


selected_grades = st.sidebar.multiselect(

    "Grade",

    grade_list,

    default=grade_list

)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    df["department"].astype(str).isin(
        selected_departments
    )
    &
    df["gender"].astype(str).isin(
        selected_genders
    )
    &
    df["grade"].astype(str).isin(
        selected_grades
    )
].copy()


# =========================================================
# CHECK FILTER RESULT
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No students match the selected filters."
    )

    st.stop()


# =========================================================
# MAIN KPI CARDS
# =========================================================

st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "👨‍🎓 Students",
    len(filtered_df)
)


col2.metric(
    "📊 Average Marks",
    f"{filtered_df['marks'].mean():.2f}"
)


col3.metric(
    "🏆 Highest Marks",
    f"{filtered_df['marks'].max():.0f}"
)


col4.metric(
    "📅 Avg Attendance",
    f"{filtered_df['attendance'].mean():.2f}%"
)


col5.metric(
    "🏫 Departments",
    filtered_df["department"].nunique()
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(

    [
        "📋 Data Overview",
        "📊 Statistics",
        "🏆 Top Students",
        "📈 Graphs",
        "📝 Findings"
    ]

)


# =========================================================
# TAB 1
# DATA OVERVIEW
# =========================================================

with tab1:

    st.header("📋 Dataset Overview")


    # Preview

    st.subheader("Dataset Preview")

    st.dataframe(

        filtered_df.head(10),

        use_container_width=True

    )


    # Complete dataset

    st.subheader("Complete Dataset")

    st.dataframe(

        filtered_df,

        use_container_width=True,

        height=400

    )


    # -----------------------------------------------------
    # DATA INFORMATION
    # -----------------------------------------------------

    st.subheader("🔍 Dataset Information")


    info_df = pd.DataFrame({

        "Column":
            filtered_df.columns,

        "Data Type":
            filtered_df.dtypes.astype(str),

        "Non-Null":
            filtered_df.notna().sum().values,

        "Missing":
            filtered_df.isna().sum().values

    })


    st.dataframe(

        info_df,

        use_container_width=True

    )


    # -----------------------------------------------------
    # MISSING VALUES
    # -----------------------------------------------------

    st.subheader(
        "❓ Missing Value Analysis"
    )


    missing_values = filtered_df.isnull().sum()


    missing_df = pd.DataFrame({

        "Column":
            missing_values.index,

        "Missing Values":
            missing_values.values

    })


    st.dataframe(

        missing_df,

        use_container_width=True

    )


    total_missing = missing_values.sum()


    if total_missing == 0:

        st.success(
            "✅ No missing values found."
        )

    else:

        st.warning(
            f"⚠️ Total missing values: "
            f"{total_missing}"
        )


    # -----------------------------------------------------
    # DUPLICATES
    # -----------------------------------------------------

    st.subheader(
        "🔁 Duplicate Records"
    )


    duplicate_count = filtered_df.duplicated().sum()


    if duplicate_count == 0:

        st.success(
            "✅ No duplicate records found."
        )

    else:

        st.warning(
            f"⚠️ {duplicate_count} duplicate "
            f"records found."
        )


# =========================================================
# TAB 2
# STATISTICS
# =========================================================

with tab2:

    st.header("📊 Key Statistics")


    # -----------------------------------------------------
    # BASIC STATISTICS
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)


    c1.metric(

        "Average Marks",

        f"{filtered_df['marks'].mean():.2f}"

    )


    c2.metric(

        "Highest Marks",

        f"{filtered_df['marks'].max():.0f}"

    )


    c3.metric(

        "Lowest Marks",

        f"{filtered_df['marks'].min():.0f}"

    )


    c4.metric(

        "Average Attendance",

        f"{filtered_df['attendance'].mean():.2f}%"

    )


    # -----------------------------------------------------
    # MARKS STATISTICS
    # -----------------------------------------------------

    st.subheader(
        "📚 Marks Statistics"
    )


    marks_stats = (

        filtered_df["marks"]

        .describe()

        .round(2)

    )


    st.dataframe(

        marks_stats.to_frame(
            "Value"
        ),

        use_container_width=True

    )


    # -----------------------------------------------------
    # ATTENDANCE STATISTICS
    # -----------------------------------------------------

    st.subheader(
        "📅 Attendance Statistics"
    )


    attendance_stats = (

        filtered_df["attendance"]

        .describe()

        .round(2)

    )


    st.dataframe(

        attendance_stats.to_frame(
            "Value"
        ),

        use_container_width=True

    )


    # -----------------------------------------------------
    # DEPARTMENT STATISTICS
    # -----------------------------------------------------

    st.subheader(
        "🏫 Department-wise Statistics"
    )


    department_stats = (

        filtered_df

        .groupby("department")

        .agg(

            Students=(
                "roll_no",
                "count"
            ),

            Average_Marks=(
                "marks",
                "mean"
            ),

            Highest_Marks=(
                "marks",
                "max"
            ),

            Average_Attendance=(
                "attendance",
                "mean"
            )

        )

        .round(2)

        .sort_values(
            "Average_Marks",
            ascending=False
        )

    )


    st.dataframe(

        department_stats,

        use_container_width=True

    )


# =========================================================
# TAB 3
# TOP STUDENTS
# =========================================================

with tab3:

    st.header(
        "🏆 Top-Performing Students"
    )


    number = st.slider(

        "Number of students",

        min_value=5,

        max_value=min(
            20,
            len(filtered_df)
        ),

        value=min(
            10,
            len(filtered_df)
        )

    )


    top_students = (

        filtered_df

        .sort_values(

            ["marks", "attendance"],

            ascending=False

        )

        .head(number)

    )


    st.dataframe(

        top_students[

            [

                "roll_no",

                "name",

                "gender",

                "age",

                "marks",

                "attendance",

                "department",

                "grade"

            ]

        ],

        use_container_width=True

    )


    # -----------------------------------------------------
    # TOP STUDENT
    # -----------------------------------------------------

    st.subheader(
        "🥇 Highest-Scoring Student"
    )


    top_student = filtered_df.loc[

        filtered_df["marks"].idxmax()

    ]


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Name",
        str(top_student["name"])
    )


    c2.metric(
        "Marks",
        int(top_student["marks"])
    )


    c3.metric(
        "Attendance",
        f"{top_student['attendance']}%"
    )


    c4.metric(
        "Grade",
        str(top_student["grade"])
    )


# =========================================================
# TAB 4
# GRAPHS
# =========================================================

with tab4:

    st.header(
        "📈 Student Data Visualizations"
    )


    # =====================================================
    # GRAPH 1
    # MARKS DISTRIBUTION
    # =====================================================

    st.subheader(
        "1️⃣ Distribution of Student Marks"
    )


    fig1, ax1 = plt.subplots(
        figsize=(9, 5)
    )


    ax1.hist(

        filtered_df["marks"].dropna(),

        bins=10,

        edgecolor="black"

    )


    ax1.set_title(
        "Distribution of Student Marks"
    )


    ax1.set_xlabel(
        "Marks"
    )


    ax1.set_ylabel(
        "Number of Students"
    )


    ax1.grid(
        axis="y",
        alpha=0.3
    )


    st.pyplot(
        fig1,
        use_container_width=True
    )


    plt.close(fig1)


    # =====================================================
    # GRAPH 2
    # GRADE DISTRIBUTION
    # =====================================================

    st.subheader(
        "2️⃣ Grade Distribution"
    )


    grade_counts = (
    df["grade"]
    .value_counts()
    .reset_index()
)