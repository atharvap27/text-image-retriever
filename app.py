# import streamlit as st
# from multimodal_search import MultimodalSearch

# st.set_page_config(
#     layout="wide"
# )

# def main():
#     st.markdown("<h1 style='text-align: center; color: green;'>Fashion Cloth Search App</h1>", unsafe_allow_html=True)

#     multimodal_search = MultimodalSearch()

    # query = st.text_input("Enter your query:")
    # if st.button("Search"):
    #     if len(query) > 0:
    #         results = multimodal_search.search(query)
    #         st.warning("Your query was "+query)
    #         st.subheader("Search Results:")
    #         col1, col2, col3 = st.columns([1,1,1])
    #         with col1:
    #             st.write(f"Score: {round(results[0].score*100, 2)}%")
    #             st.image(results[0].content, use_column_width=True)
    #         with col2:
    #             st.write(f"Score: {round(results[1].score*100, 2)}%")
    #             st.image(results[1].content, use_column_width=True)
    #         with col3:
    #             st.write(f"Score: {round(results[2].score*100, 2)}%")
    #             st.image(results[2].content, use_column_width=True)
    #     else:
    #         st.warning("Please enter a query.")

# if __name__ == "__main__":
#     main()




import streamlit as st
from multimodal_search import MultimodalSearch
from google_auth import google_login

def main():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center; color: green;'>FindMe.ai</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: green;'>Find anything in your photos using text</h1>", unsafe_allow_html=True)

    # Button to initiate OAuth process
    if st.button('Connect to Google Photos'):
        creds = google_login()
        st.session_state['creds'] = creds
        st.success('Successfully connected to Google Photos!')

    if 'creds' in st.session_state and st.session_state['creds']:
        multimodal_search = MultimodalSearch()

        # query = st.text_input("Enter your query:")
        # if st.button("Search"):
        #     if len(query) > 0:
        #         results = multimodal_search.search(query)
        #         if results:
        #             st.subheader("Search Results:")
        #             for i, result in enumerate(results[:3]):
        #                 col = st.columns([)[i]
        #                 with col:
        #                     st.write(f"Score: {round(result.score * 100, 2)}%")
        #                     st.image(result.content, use_column_width=True)
        #         else:
        #             st.warning("No results found.")
        #     else:
                # st.warning("Please enter a query.")

        query = st.text_input("Enter your query:")
        if st.button("Search"):
            if len(query) > 0:
                results = multimodal_search.search(query)
                st.warning("Your query was "+query)
                st.subheader("Search Results:")
                col1, col2, col3 = st.columns([1,1,1])
                with col1:
                    st.write(f"Score: {round(results[0].score*100, 2)}%")
                    st.image(results[0].content, use_column_width=True)
                with col2:
                    st.write(f"Score: {round(results[1].score*100, 2)}%")
                    st.image(results[1].content, use_column_width=True)
                with col3:
                    st.write(f"Score: {round(results[2].score*100, 2)}%")
                    st.image(results[2].content, use_column_width=True)
            else:
                st.warning("Please enter a query.")
    else:
        st.warning("Please connect to Google Photos to use the search functionality.")

if __name__ == "__main__":
    main()


