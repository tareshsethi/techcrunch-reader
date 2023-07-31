import os
import uuid

import requests
import streamlit as st

BACKEND_JWT = os.environ.get('BACKEND_JWT', '')
BACKEND_URL = os.environ.get('BACKEND_URL', '')


def create_msg_with_sources(response, sources_urls):
    msg = response
    sources_str = ','.join(
        [f'[[{num + 1}]({source_url})]' for num, source_url in enumerate(sources_urls)]
    )
    return f'{msg}\n\nSources: {sources_str}'


def main():
    st.set_page_config(page_title="TechCrunch Reader", page_icon="🌱")

    st.title("💬 TechCrunch (Startups) Reader")
    st.info(
        "Trained on data since July 27th, 2023. Updated daily 😅. Open TechCrunch Startups [up](https://techcrunch.com/category/startups) and have a blast"
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "How can I help you parse through TechCrunch (Startups) today?",
            }
        ]
        st.session_state['session_id'] = str(uuid.uuid4())

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        r = requests.post(
            BACKEND_URL,
            headers={'Authorization': f'Bearer {BACKEND_JWT}'},
            json={'message': prompt, 'session_id': st.session_state['session_id']},
        )
        if r.status_code == 201:
            result = r.json()
            msg = create_msg_with_sources(
                result['chatbot_response'], result['source_urls']
            )
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)


if __name__ == '__main__':
    main()
