import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

# Load the data from dataset.csv to DataFrame Pandas
main_df = pd.read_csv('dashboard/main_data.csv')

# Create a mapping for seasons to readable labels
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
main_df['season'] = main_df['season'].map(season_mapping)

# To create an order of seasons
season_order = ['Spring', 'Summer', 'Fall', 'Winter']
main_df['season'] = pd.Categorical(main_df['season'], categories=season_order, ordered=True)

# Calculate the average normalized temperature and normalized feeling temperature for each season
average_temp = main_df.groupby('season', observed=False).agg({'temp': 'mean', 'atemp': 'mean'}).reset_index()

# Melt the DataFrame for easier plotting
average_temp_melted = average_temp.melt(id_vars='season', value_vars=['temp', 'atemp'],
                                         var_name='Temperature Types', value_name='Average Temperature')

# To replace the temperature type label to be readable by the general public
average_temp_melted['Temperature Types'] = average_temp_melted['Temperature Types'].replace({
    'temp': 'Normalized Temperature (°C)',
    'atemp': 'Normalized Feeling Temperature (°C)'
})

# Create a new column to interpret hours as day type
main_df['time_of_day'] = main_df['hr'].apply(lambda x: 'Morning' if x <= 12 else 'Evening/Night')

# Set the order from morning to evening/night
main_df['time_of_day'] = pd.Categorical(main_df['time_of_day'], categories=['Morning', 'Evening/Night'], ordered=True)

# To create a bar graph
total_rentals = main_df.groupby('time_of_day', observed=False)['cnt'].count()

# Setting streamlit CSS styles
st.markdown(
    """
    <style>
    .justify-text {
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a dashboard title 
st.markdown("<h1 style='text-align: center;'>Bike Sharing Dataset<br>Analysis Dashboard</h1>", unsafe_allow_html=True)

# Create two columns for personal identity and graphs
col1, col2 = st.columns([2, 3])

# Personal identity column
with col1:
    st.header("Personal Identity")
    st.write("Nama: Wilson Leonardo")
    st.write("Email: wilsonleonardo4002@gmail.com")
    st.write("ID Dicoding: wileo2004")
    st.write("GitHub: https://github.com/AlicelieseLou/Dicoding_Submission.git")

# Graph column
with col2:
    st.header("My Visualization Data")
    # Create tabs for each graph
    tab1, tab2 = st.tabs(
                        ["First Visualization",
                        "Second Visualization"])

    # Visualization Comparison of Normalized Temperature and Normalized Feeling Temperature by Season
    with tab1:
        st.markdown("<p class='justify-text'>Bagaimana perubahan musim mempengaruhi hubungan antara suhu normalisasi dan suhu normalisasi yang dirasakan?</p>", unsafe_allow_html=True)
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=average_temp_melted, x='season', y='Average Temperature', hue='Temperature Types', marker='o')
        plt.title('Comparison of Normalized Temperature and Normalized Feeling Temperature by Season', fontweight='bold')
        plt.xlabel('Season')
        plt.ylabel('Average Normalized Temperature')
        plt.grid()
        plt.xticks(rotation=45)
        plt.legend(title='Temperature Types')
        plt.tight_layout()

        # Display the graph in Streamlit
        st.pyplot(plt)

        # Show the conclusion
        with st.expander("Show Conclustion"):
            st.markdown("<p class='justify-text'>Perubahan musim cenderung mengalami perubahan suhu normalisasi dan suhu normalisasi yang dirasakan secara signifikan, terlihat bahwa suhu normalisasi meningkat secara konsisten dari musim Spring ke musim Summer dan mencapai puncaknya pada musim Fall, sebelum menurun di musim Winter. Hal ini menunjukkan bahwa suhu normalisasi dan suhu normalisasi yang dirasakan oleh individu dipengaruhi oleh kondisi musim atau faktor lingkungan.</p>", unsafe_allow_html=True)

    # Visualization Total Bike Rentals: Morning vs Evening/Night
    with tab2:
        st.markdown("<p class='justify-text'>Apakah ada perbedaan besar dalam penyewaan sepeda pada jam pagi (0-12) dan sore/malam (13-23)?</p>", unsafe_allow_html=True)

        plt.figure(figsize=(12, 6))
        bars = total_rentals.plot(kind='bar', color=['skyblue', 'orange'])
        plt.title('Total Bike Rentals: Morning vs Evening/Night', fontweight='bold')
        plt.xlabel('Time of Day')
        plt.ylabel('Total Number of Bike Rentals')
        plt.xticks(rotation=0)

        # To create exact values ​​in a bar graph
        for bar in bars.patches:
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                int(bar.get_height()),
                ha='center',
                va='bottom'
            )

        # Calculate and display the overall total rentals
        total_rentals_sum = total_rentals.sum()
        plt.text(0.5, -0.15, f'Total Rentals: {total_rentals_sum} Persons',
                ha='center', va='top', transform=plt.gca().transAxes, fontsize=12, color='black', fontweight='bold')

        # Display the graph in Streamlit
        st.pyplot(plt)

        # Show the conclusion
        with st.expander("Show Conclustion"):
            st.markdown("<p class='justify-text'>Total penyewaan sepeda di Pagi hari cenderung lebih tinggi menghasilkan nilai sebesar 9364 orang dibandingkan Sore/Malam hari yang menghasilkan nilai 8015 orang sehingga dapat memungkinkan karena disebabkan oleh faktor tertentu seperti hari masuk atau rutinitas Pagi hari dimana orang cenderung menggunakan sepeda untuk berangkat bekerja, berangkat sekolah maupun berolahraga. Sebaliknya, penyewaan di Sore/Malam hari cenderung lebih rendah juga dapat memungkinkan karena disebabkan oleh faktor tertentu seperti suhu yang cukup dingin di malam hari dan sebagainya.</p>", unsafe_allow_html=True)
