st.session_state.uploaded_files = []
            st.session_state.active_file_idx = 0
            st.session_state.active_page_idx = 0
            st.rerun()

    if st.session_state.messages:
        st.download_button(
            "📄 Download report",
            generate_report(),
            file_name=f"PlanChat_Report_{datetime.now():%Y-%m-%d}.txt",
            mime="text/plain",
            use_container_width=True,
        )

left_col, right_col = st.columns([3, 2], gap="medium")

with left_col:
    st.markdown("#### 📐 Drawing viewer")
    files = st.session_state.uploaded_files
    if not files:
        st.info("Upload plans in the sidebar to begin.")
    else:
        file_idx = min(st.session_state.active_file_idx, len(files) - 1)
        active_file = files[file_idx]
        st.session_state.active_file_idx = file_idx

        if active_file["page_count"] > 1:
            page_idx = st.slider(
                "Page",
                1,
                active_file["page_count"],
                st.session_state.active_page_idx + 1,
                key=f"page_{file_idx}",
            ) - 1
        else:
            page_idx = 0

        st.session_state.active_page_idx = page_idx
        st.image(
            active_file["pages"][page_idx],
            use_container_width=True,
            caption=f"{active_file['name']} · page {page_idx + 1}",
        )

with right_col:
    st.markdown("#### 💬 Ask PlanChat")
    chat_container = st.container(height=480)

    with chat_container:
        for msg in st.session_state.messages:
            css = "user-bubble" if msg["role"] == "user" else "model-bubble"
            body = (
                html.escape(msg["text"])
                if msg["role"] == "user"
                else render_with_citations(msg["text"])
            )
            st.markdown(f'<div class="{css}">{body}</div>', unsafe_allow_html=True)

    has_files = bool(st.session_state.uploaded_files)
    input_col, button_col = st.columns([5, 1])
    with input_col:
        user_input = st.text_input(
            "Message",
            placeholder="Ask about the drawings..." if has_files else "Upload plans first",
            disabled=not has_files,
            label_visibility="collapsed",
            key="chat_input",
        )
    with button_col:
        send = st.button(
            "Send",
            disabled=not has_files or not user_input.strip(),
            use_container_width=True,
        )

    if send and user_input.strip():
        user_text = user_input.strip()
        st.session_state.messages.append({
            "role": "user",
            "text": user_text,
            "timestamp": datetime.now().timestamp(),
        })

        full_response = ""
        response_placeholder = chat_container.empty()
        with st.spinner("Thinking..."):
            for chunk in stream_ollama_response(build_ollama_messages(user_text)):
                full_response += chunk
                response_placeholder.markdown(
                    f'<div class="model-bubble">{render_with_citations(full_response)} ▌</div>',
                    unsafe_allow_html=True,
                )

        response_placeholder.markdown(
            f'<div class="model-bubble">{render_with_citations(full_response)}</div>',
            unsafe_allow_html=True,
        )
        st.session_state.messages.append({
            "role": "model",
            "text": full_response,
            "timestamp": datetime.now().timestamp(),
        })
        st.rerun()
