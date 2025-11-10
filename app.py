"""Streamlit application for executing Griptape Nodes workflows."""

import asyncio
import logging

import streamlit as st
from dotenv import load_dotenv

from published_nodes_workflow import aexecute_workflow

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Griptape Nodes Workflow Runner",
    page_icon="🤖",
    layout="centered",
)


async def execute_workflow_async(prompt: str) -> dict[str, str]:
    """Execute the Griptape Nodes workflow with the given prompt.

    Args:
        prompt: The user's input prompt to send to the Agent.

    Returns:
        dict: Contains 'output', 'was_successful', 'result_details' keys.
    """
    if not prompt.strip():
        return {
            "output": "",
            "was_successful": "false",
            "result_details": "Error: Prompt cannot be empty",
        }

    flow_input = {
        "Start Flow": {
            "prompt": prompt,
        }
    }

    try:
        output = await aexecute_workflow(input=flow_input)

        if output is None:
            return {
                "output": "",
                "was_successful": "false",
                "result_details": "Error: Workflow did not produce output",
            }

        end_flow_data = output.get("End Flow", {})

        return {
            "output": end_flow_data.get("output", ""),
            "was_successful": str(end_flow_data.get("was_successful", False)).lower(),
            "result_details": end_flow_data.get("result_details", ""),
        }

    except Exception as e:
        logger.exception("Workflow execution failed")
        return {
            "output": "",
            "was_successful": "false",
            "result_details": f"Error: {e!s}",
        }


def execute_workflow(prompt: str) -> dict[str, str]:
    """Synchronous wrapper for async workflow execution.

    Args:
        prompt: The user's input prompt to send to the Agent.

    Returns:
        dict: Contains 'output', 'was_successful', 'result_details' keys.
    """
    return asyncio.run(execute_workflow_async(prompt))


def main() -> None:
    """Main Streamlit application."""
    st.title("🤖 Griptape Nodes Workflow Runner")
    st.markdown("Execute AI agent workflows with a simple interface")

    # Input section
    prompt = st.text_area(
        "Enter your prompt:",
        placeholder="Type your message to the agent here...",
        height=100,
        key="prompt_input",
    )

    # Run button
    if st.button("Run Workflow", type="primary", use_container_width=True):
        if not prompt.strip():
            st.error("Please enter a prompt")
        else:
            with st.spinner("Running workflow..."):
                result = execute_workflow(prompt)

            # Display results
            st.markdown("---")
            st.subheader("Output:")

            if result["was_successful"] == "true":
                st.success("✓ Success")
                st.markdown(result["output"] if result["output"] else "_No output returned_")
            else:
                st.error("✗ Failed")
                st.markdown(result["output"] if result["output"] else "_Workflow failed to produce output_")

            # Show details if present
            if result["result_details"]:
                with st.expander("Details"):
                    st.text(result["result_details"])


if __name__ == "__main__":
    main()
