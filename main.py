import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide"
)

# Title
st.title("Exploratory Data Analysis Dashboard")
st.write("Upload a CSV file to explore and visualize your dataset.")




# SIDEBAR
st.sidebar.header("Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)


# MAIN PROGRAM
if uploaded_file is not None:

    # Read CSV file
    df = pd.read_csv(uploaded_file)

    st.success("CSV file uploaded successfully!")

    
    # DATASET PREVIEW
    st.header("Dataset Preview")

    st.dataframe(df.head())

   
    # DATASET DIMENSIONS
    st.header("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Number of Rows", df.shape[0])

    with col2:
        st.metric("Number of Columns", df.shape[1])


    # DATA TYPES
    st.subheader("Column Data Types")

    datatype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(datatype_df)


    # MISSING VALUES
    st.subheader("Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing_df)

    # STATISTICS
    st.subheader("Numerical Statistics")

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numerical_columns) > 0:

        statistics = pd.DataFrame({
            "Mean": df[numerical_columns].mean(),
            "Median": df[numerical_columns].median(),
            "Minimum": df[numerical_columns].min(),
            "Maximum": df[numerical_columns].max()
        })

        st.dataframe(statistics)


    # ATTRIBUTE SELECTION
    st.header("Attribute Visualization")

    selected_column = st.sidebar.selectbox(
        "Select a column",
        df.columns
    )

    # AUTOMATIC TYPE DETECTION
    if pd.api.types.is_numeric_dtype(df[selected_column]):

        st.subheader("Numerical Attribute")

        st.write("Selected column:", selected_column)

        # Histogram
        fig, ax = plt.subplots()

        ax.hist(
            df[selected_column].dropna(),
            bins=20
        )

        ax.set_title(
            "Distribution of " + selected_column
        )

        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

    else:

        st.subheader("Categorical Attribute")

        st.write("Selected column:", selected_column)

        # Frequency count
        counts = df[selected_column].value_counts()

        # Bar chart
        fig, ax = plt.subplots()

        counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Frequency of " + selected_column
        )

        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

else:

    st.info("Please upload a CSV file from the sidebar.")