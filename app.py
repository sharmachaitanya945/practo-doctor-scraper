import requests
from bs4 import BeautifulSoup
import streamlit as st
import urllib.parse
import json

# Add favicon and title to the page

st.set_page_config(
    page_title="Practo Doctor Scraper",
    page_icon="🩺",
)
st.image("logo.png", width=400, caption="Practo Doctor Scraper", use_column_width=False, output_format='auto', channels='RGB')
st.logo("logo.png")
# Toggle button for markdown content
if 'show_markdown' not in st.session_state:
    st.session_state.show_markdown = False

if st.button("Read Me"):
    st.session_state.show_markdown = not st.session_state.show_markdown

# Conditionally render markdown content
if st.session_state.show_markdown:
    st.markdown(
        """
        
        # 🩺 Practo Doctor Scraper

        Welcome to the Practo Doctor Scraper! This application allows you to scrape information about doctors from Practo based on specialization, locality, and city. It displays the total number of doctors available for the selected specialization and location.

        ## 🌟 Features

        - 🩺 **Specialization Selection**: Choose a medical specialization to search for doctors.
        - 🏠 **Locality Input**: Enter the locality where you want to search for doctors.
        - 🌆 **City Input**: Enter the city for your search.
        - 🔍 **Doctor Count**: Displays the total number of doctors available based on your search criteria.
        - 🌐 **Dynamic URL Construction**: Constructs and logs the URL used to retrieve data.
        - ❌ **Error Handling**: Informs the user if the data could not be retrieved.

        ## 📸 Screenshots

        Add relevant screenshots here to showcase the user interface.

        ## 🛠️ Technologies Used

        - ⚛️ **Streamlit**: For the web interface.
        - 🌐 **BeautifulSoup**: For parsing the HTML content.
        - 📝 **Requests**: For sending HTTP requests to Practo.

        ## 📦 Installation

        1. Clone the repository:
            ```bash
            git clone https://github.com/sharmachaitanya945/paidintern.git
            ```
        2. Navigate to the project directory:
            ```bash
            cd practo-doctor-scraper
            ```
        3. Install the required packages:
            ```bash
            pip install -r requirements.txt
            ```
        4. Run the Streamlit app:
            ```bash
            streamlit run app.py
            ```

        ## 🚀 Usage

        1. Select a specialization from the dropdown menu.
        2. Enter the locality and city where you want to search for doctors.
        3. Click the "Scrape" button to fetch and display the total number of doctors in the specified area.

        ## 📜 License

        This project is licensed under the MIT License.

        ## 🙌 Acknowledgements

        - 🌐 [Practo](https://www.practo.com/) for the data.
        - 🧙‍♂️ [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
        - ⚛️ [Streamlit](https://streamlit.io/) for the web framework.

        ## 🤝 Contributing

        Contributions are welcome! Open an issue or submit a pull request for any improvements or suggestions.
        """
    )

# Inputs
specialization = st.selectbox("Select Specialization", ["Cardiologist", "Dentist", "Dermatologist", "General Physician", "Gynecologist","Ayurveda","Ear-nose-throat (ent) Specialist"])
locality = st.text_input("Enter Locality")
city = st.text_input("Enter City")

def scrape_total_doctors(specialization, locality, city):
    # Construct the base URL
    query = [
        {"word": specialization, "autocompleted": True, "category": "subspeciality"},
        {"word": locality, "autocompleted": True, "category": "locality"}
    ]
    query_encoded = urllib.parse.quote(json.dumps(query))
    base_url = f"https://www.practo.com/search/doctors?results_type=doctor&q={query_encoded}&city={city.lower()}"
    
    st.write(f"Constructed URL: {base_url}")  # Log the constructed URL
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send GET request
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract total number of doctors
        total_doctors_element = soup.find("h1", class_="u-xx-large-font u-bold")
        if total_doctors_element:
            total_doctors = total_doctors_element.text.strip()
            st.markdown(f"<h2 style='text-align: center; color: blue;'>Total {specialization}s: {total_doctors}</h2>", unsafe_allow_html=True)
        else:
            st.write("Could not find the total number of doctors.")
    else:
        st.write(f"Failed to retrieve data. Status code: {response.status_code}")

# Scrape Button
if st.button("Scrape"):
    scrape_total_doctors(specialization, locality, city)

# Footer
st.markdown(
    """
    <hr>
    <div style="text-align: center;">
        <p>⭐ If you found this helpful, please consider giving it a star! ⭐</p>
        <p>Made with ❤️  by <a href="https://github.com/sharmachaitanya945" target="_blank">Chaitanya Sharma</a></p>
        <p>Project Submitted to <a href="https://www.linkedin.com/company/paidintern/" target="_blank">PaidIntern</a></p>    </div>
    """,
    unsafe_allow_html=True
)