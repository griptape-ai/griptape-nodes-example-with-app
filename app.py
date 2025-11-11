"""Streamlit application for executing Griptape Nodes workflows."""

import asyncio
import json
import logging

import streamlit as st
from dotenv import load_dotenv
from griptape_nodes.bootstrap.workflow_executors.local_workflow_executor import LocalWorkflowExecutor
from griptape_nodes.drivers.storage.storage_backend import StorageBackend
from griptape_nodes.retained_mode.events.flow_events import GetTopLevelFlowRequest, GetTopLevelFlowResultSuccess
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Griptape Nodes Audio Generation",
    page_icon="🎵",
    layout="wide",
)

# Import the workflow to initialize it (module imported for side effects)
import published_nodes_workflow  # noqa: F401, E402 # pyright: ignore[reportUnusedImport]


def _ensure_workflow_context() -> None:
    """Ensure the workflow context is properly set up."""
    context_manager = GriptapeNodes.ContextManager()
    if not context_manager.has_current_flow():
        top_level_flow_request = GetTopLevelFlowRequest()
        top_level_flow_result = GriptapeNodes.handle_request(top_level_flow_request)
        if isinstance(top_level_flow_result, GetTopLevelFlowResultSuccess) and top_level_flow_result.flow_name is not None:
            flow_manager = GriptapeNodes.FlowManager()
            flow_obj = flow_manager.get_flow_by_name(top_level_flow_result.flow_name)
            context_manager.push_flow(flow_obj)


@st.cache_resource
def get_workflow_executor() -> LocalWorkflowExecutor:
    """Initialize and return a cached LocalWorkflowExecutor instance.

    This ensures the executor is initialized only once and reused across runs.
    """
    storage_backend_enum = StorageBackend.LOCAL
    return LocalWorkflowExecutor(storage_backend=storage_backend_enum)


def _initialize_session_state() -> None:  # noqa: C901
    """Initialize all session state variables with default values."""
    # Text area defaults (placeholders until user provides actual defaults)
    if "world_rules" not in st.session_state:
        st.session_state.world_rules = """It is the 2650s. The Terran Confederation Space Force is in a desperate war with an aggressive race of cat-like aliens called the Kilrathi.

Each part of the campaign takes place across multiple systems in space. Within a system, fighter teams make multiple sorties against the Kilrathi. Depending on how these sorties perform, they will either win or lose the system, affecting the outcome of the campaign."""

    if "character_definition" not in st.session_state:
        st.session_state.character_definition = """You are Colonel Peter Halcyon of the TCS Tiger's Claw.

Your duty is to oversee sorties of fighters in the ongoing war. You assign missions and evaluate performance.

Each sortie has a wing commander, usually with one or more wingmen.

You are stern, but caring. You have a rag-tag team that you need to develop into effective leaders.

You do not mince words. You speak about the enemy in dehumanizing terms ("cats", "furballs", etc.) to galvanize your team.

The loss of pilots is inexcusable and you do not tolerate poor leadership that leads to the loss of life.

You prioritize the mission objectives, the safety of your pilots, utilizing tactics to eliminate enemies while minimizing danger, and the condition of the machines they bring back.

You deliver a mission summary to the members of a sortie. Your top priority is the primary mission objectives and how well the sortie did or did not fulfill them.
Next, you want to lay out secondary objectives and how the team performed with them.

Next, you want to relay how the wing commander performed in their role. You need to address how they acted as a leader, and how they treated their wingmen. Losing a wingman is a severe morale loss, so you want to stress strong leadership that emphasizes teamwork.

Finally, you want to discuss how the team performed in combat, and ask them how to improve. Assess their tactics and how they executed."""

    if "data_expert_1" not in st.session_state:
        st.session_state.data_expert_1 = """You are an expert describing the objectives of a mission and whether they were met or not.

Describe the mission and its objectives (including secondary objectives).

Based on the facts that you have, assess whether the objectives were met or not.

You are only given facts as a JSON table."""

    if "data_expert_2" not in st.session_state:
        st.session_state.data_expert_2 = """You are an expert on summarizing encounters that happened during a military sortie.

Describe the encounters that occurred during the mission. Place the encounters in context of the mission plan, if there was one.

Describe each encounter in terms of what the sortie discovered, how many and what types of others were encountered, how they responded. This should include the rules of engagement employed, how the sortie was deployed to engage, and how enemies were dispatched.

If ships were damaged or destroyed, report on that. If key people from the mission objectives were impacted, report on that.

For any combat engagement, describe the outcome. If ships were damaged or destroyed, explain how and by what means.

If combat did not occur at a specified waypoint, mention that.

You are only given facts as a JSON table."""

    if "data_expert_3" not in st.session_state:
        st.session_state.data_expert_3 = """You are an expert on assessing a sortie's ability to act as an effective team. Do not focus on summarizing overall mission objectives; we are focused on individuals and how they contributed to operating as a team.

Based on the data provided, describe the team's coordination. This should include the squad's tactics and outcomes.

Assess each participant's performance as well as their effectiveness as a whole. How did they communicate? Did they exercise solid judgment?

Of particular emphasis will be the effectiveness of the wing commander (leader). How well did they coordinate their squadron and respond as things changed? Will they maintain morale if they continue in this role? Did they make the correct judgment calls for themselves and their squad? Were the risks taken justified?

Be sure to summarize the contributions of each friendly participant. Where did they excel? How can they improve?

You are only given facts as a JSON table."""

    if "summarizer" not in st.session_state:
        st.session_state.summarizer = """You are providing a mission summary to the Lt. Colonel for them to deliver to the wing that just flew the sortie.

Summarize the breakdowns each of the experts provided."""

    if "speechwriter_rules" not in st.session_state:
        st.session_state.speechwriter_rules = "Generate a mission summary for the wing commander and any wingmen they may have had under them during this mission."

    if "acting_coach_rules" not in st.session_state:
        st.session_state.acting_coach_rules = """Based on what you know about this character, create an audio text-to-speech prompt that captures the character's tone and mood for this mission debriefing.

You will be altering the original mission briefing by inserting audio tags and adjusting punctuation and capitalization to convey tone and pacing.

Audio tags are supplied in [brackets]. These will be used to express how the line is delivered. Only use a single tag at a time; if you want to add both "stern" and "commanding", inject them as [stern][commanding].

Audio tags can also be used for pacing. [sighs] and [exhales] can convey the speaker's mood, for example.

Ellipses and capitalized words can be used to adjust pacing and delivery."""

    if "music_coach_rules" not in st.session_state:
        st.session_state.music_coach_rules = """This music will be used behind dialogue delivery. It should not overwhelm the dialogue. We are here to convey a tone and mood within a tense and dangerous environment.

It is there to ENHANCE the delivery of the dialogue, not to distract from it.

The music should not have words.

Based on the mission summary delivered, generate a music generation prompt that reflects the tone of the commander."""

    if "game_data_json" not in st.session_state:
        st.session_state.game_data_json = """{
  "location": "Deneb system",
  "mission_type": "Patrol",
  "primary_objectives": {
    "patrol_waypoints": [
      1,
      2,
      3,
      4
    ]
  },
  "secondary_objectives": [
    "eliminate Dorkhir tanker"
  ],
  "sortie_squadron": [
    {
      "name": "Christopher Blair",
      "rank": "2nd Lieutenant",
      "callsign": "Bluehair",
      "role": "Wing Commander",
      "ship": "Hornet"
    },
    {
      "name": "Tanaka Mariko",
      "rank": "Lieutenant",
      "callsign": "Spirit",
      "role": "wingman",
      "ship": "Hornet"
    }
  ],
  "performance": {
    "waypoints_visited": [
      1,
      2,
      3,
      4
    ],
    "encounters": [
      {
        "location": "en route to waypoint 2 from waypoint 1",
        "enemy_count": 4,
        "enemy_type": "Kilrathi fighters",
        "outcome": {
          "destroyed_by_blair": 3,
          "methods": {
            "IR_missiles": 2,
            "laser_guns": 1
          },
          "damaged_by_spirit": 1,
          "escaped": 1
        }
      },
      {
        "location": "waypoint 2",
        "hazard": "asteroid field",
        "incident": "Blair collided with asteroid, one gun damaged",
        "decision": "mission continued"
      },
      {
        "location": "en route to waypoint 3",
        "target": "Dorkhir tanker",
        "guards": {
          "type": "heavy fighters",
          "count": 3
        },
        "decision": "engage",
        "outcome": {
          "tanker": {
            "destroyed_by": "Blair",
            "weapons_used": [
              "dumbfire missiles",
              "guns"
            ]
          },
          "guards": {
            "destroyed_by_spirit": 2,
            "methods": [
              "guns",
              "missiles"
            ],
            "escaped": 1
          },
          "casualties": {
            "spirit_ship": "destroyed by enemy collision",
            "spirit_pilot": "ejected"
          }
        }
      },
      {
        "location": "waypoint 3",
        "enemy_activity": "none"
      },
      {
        "location": "waypoint 4",
        "enemy_activity": "none"
      }
    ],
    "kills": {
      "blair": 4,
      "spirit": 2,
      "total": 6
    },
    "enemies_escaped": 2,
    "notable_events": [
      "Blair damaged ship in asteroid collision at waypoint 2",
      "Spirit's ship lost to enemy collision during tanker engagement",
      "Spirit ejected and recovered safely",
      "Tanker destroyed before jump"
    ]
  },
  "mission_results": {
    "primary_objective_status": "completed",
    "secondary_objective_status": "completed",
    "mission_outcome": "success",
    "pilot_status": {
      "blair": {
        "status": "returned",
        "ship_damage": "one gun destroyed (asteroid collision)"
      },
      "spirit": {
        "status": "recovered safely",
        "ship_status": "lost (enemy collision)",
        "present_at_debriefing": true
      }
    },
    "losses": {
      "pilots": 0,
      "ships": 1
    }
  }
}"""

    # Output state
    if "workflow_outputs" not in st.session_state:
        st.session_state.workflow_outputs = None


async def execute_workflow_async(  # noqa: PLR0913
    world_rules: str,
    character_definition: str,
    data_expert_1: str,
    data_expert_2: str,
    data_expert_3: str,
    summarizer: str,
    speechwriter_rules: str,
    acting_coach_rules: str,
    music_coach_rules: str,
    game_data: str,
) -> dict:
    """Execute the Griptape Nodes workflow with all inputs.

    Args:
        world_rules: World context and rules
        character_definition: Character definition
        data_expert_1: First data expert rules
        data_expert_2: Second data expert rules
        data_expert_3: Third data expert rules
        summarizer: Summarizer rules
        speechwriter_rules: Speechwriter guidelines
        acting_coach_rules: Acting coach guidelines
        music_coach_rules: Music coach guidelines
        game_data: JSON string of game data

    Returns:
        dict: Contains workflow output including audio artifacts, text outputs, and retrospective.
    """
    flow_input = {
        "Start Flow": {
            "world_rules": world_rules,
            "character_definition": character_definition,
            "data_expert_1": data_expert_1,
            "data_expert_2": data_expert_2,
            "data_expert_3": data_expert_3,
            "summarizer": summarizer,
            "speechwriter_rules": speechwriter_rules,
            "acting_coach_rules": acting_coach_rules,
            "music_coach_rules": music_coach_rules,
            "game_data": game_data,
        }
    }

    try:
        # Get the cached executor instance
        executor = get_workflow_executor()

        # Ensure workflow context is set up
        _ensure_workflow_context()

        # Initialize the executor context manager on first use
        if "executor_initialized" not in st.session_state:
            await executor.__aenter__()
            st.session_state.executor_initialized = True

        # Run the workflow using the existing executor
        await executor.arun(flow_input=flow_input, pickle_control_flow_result=False)

        if executor.output is None:
            return {
                "was_successful": False,
                "result_details": "Workflow did not produce output",
            }

        end_flow_data = executor.output.get("End Flow", {})

        return {
            "was_successful": end_flow_data.get("was_successful", False),
            "result_details": end_flow_data.get("result_details", ""),
            "voice_audio_artifact": end_flow_data.get("voice_audio_artifact"),
            "music_audio_artifact": end_flow_data.get("music_audio_artifact"),
            "speechwriter_output": end_flow_data.get("speechwriter_output", ""),
            "acting_coach_output": end_flow_data.get("acting_coach_output", ""),
            "retrospective": end_flow_data.get("retrospective", ""),
        }

    except Exception as e:
        logger.exception("Workflow execution failed")
        return {
            "was_successful": False,
            "result_details": f"Error: {e!s}",
        }


def main() -> None:  # noqa: PLR0915, PLR0912, C901
    """Main Streamlit application."""
    _initialize_session_state()

    st.title("🎵 Griptape Nodes Audio Generation")
    st.markdown("Generate audio content with AI-powered workflows")

    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "World",
        "Character",
        "Data Experts",
        "Speechwriter",
        "Acting Coach",
        "Music Coach",
        "Generation",
    ])

    # World tab
    with tab1:
        st.header("World Rules")
        st.session_state.world_rules = st.text_area(
            "Define the rules and context of your world:",
            value=st.session_state.world_rules,
            height=400,
            key="world_rules_input",
        )

    # Character tab
    with tab2:
        st.header("Character Definition")
        st.session_state.character_definition = st.text_area(
            "Define your character's traits, background, and personality:",
            value=st.session_state.character_definition,
            height=400,
            key="character_definition_input",
        )

    # Data Experts tab
    with tab3:
        st.header("Data Experts")

        st.subheader("Data Expert 1")
        st.session_state.data_expert_1 = st.text_area(
            "Define the first data expert's role and expertise:",
            value=st.session_state.data_expert_1,
            height=150,
            key="data_expert_1_input",
        )

        st.subheader("Data Expert 2")
        st.session_state.data_expert_2 = st.text_area(
            "Define the second data expert's role and expertise:",
            value=st.session_state.data_expert_2,
            height=150,
            key="data_expert_2_input",
        )

        st.subheader("Data Expert 3")
        st.session_state.data_expert_3 = st.text_area(
            "Define the third data expert's role and expertise:",
            value=st.session_state.data_expert_3,
            height=150,
            key="data_expert_3_input",
        )

        st.subheader("Summarizer")
        st.session_state.summarizer = st.text_area(
            "Define the summarizer's role and approach:",
            value=st.session_state.summarizer,
            height=150,
            key="summarizer_input",
        )

    # Speechwriter tab
    with tab4:
        st.header("Speechwriter Rules")
        st.session_state.speechwriter_rules = st.text_area(
            "Define how the speechwriter should craft speeches:",
            value=st.session_state.speechwriter_rules,
            height=400,
            key="speechwriter_rules_input",
        )

    # Acting Coach tab
    with tab5:
        st.header("Acting Coach Rules")
        st.session_state.acting_coach_rules = st.text_area(
            "Define how the character should deliver lines:",
            value=st.session_state.acting_coach_rules,
            height=400,
            key="acting_coach_rules_input",
        )

    # Music Coach tab
    with tab6:
        st.header("Music Coach Rules")
        st.session_state.music_coach_rules = st.text_area(
            "Define the music coaching guidelines:",
            value=st.session_state.music_coach_rules,
            height=400,
            key="music_coach_rules_input",
        )

    # Generation tab
    with tab7:
        st.header("Generate Audio")

        # Two-column layout
        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.subheader("Game Data")
            st.session_state.game_data_json = st.text_area(
                "Paste your JSON game data:",
                value=st.session_state.game_data_json,
                height=400,
                key="game_data_json_input",
            )

            # Validate JSON
            json_valid = False
            try:
                json_str = st.session_state.game_data_json or "{}"
                json.loads(json_str)  # Just validate, don't parse
                json_valid = True
                st.success("✓ Valid JSON")
            except json.JSONDecodeError as e:
                st.error(f"✗ Invalid JSON: {e.msg}")

        with col_right:
            # Run button
            if st.button(
                "Run Griptape Nodes Workflow to Generate Audio",
                type="primary",
                use_container_width=True,
                disabled=not json_valid,
            ):
                with st.spinner("Generating audio..."):
                    result = asyncio.run(
                        execute_workflow_async(
                            world_rules=st.session_state.world_rules or "",
                            character_definition=st.session_state.character_definition or "",
                            data_expert_1=st.session_state.data_expert_1 or "",
                            data_expert_2=st.session_state.data_expert_2 or "",
                            data_expert_3=st.session_state.data_expert_3 or "",
                            summarizer=st.session_state.summarizer or "",
                            speechwriter_rules=st.session_state.speechwriter_rules or "",
                            acting_coach_rules=st.session_state.acting_coach_rules or "",
                            music_coach_rules=st.session_state.music_coach_rules or "",
                            game_data=st.session_state.game_data_json or "{}",
                        )
                    )
                    st.session_state.workflow_outputs = result

            # Display outputs if available
            if st.session_state.workflow_outputs is not None:
                outputs = st.session_state.workflow_outputs

                if not outputs.get("was_successful", False):
                    st.error(f"✗ Workflow failed: {outputs.get('result_details', 'Unknown error')}")
                else:
                    st.success("✓ Audio generation complete!")

                    # Show result details if present
                    if outputs.get("result_details"):
                        st.info(outputs["result_details"])

                    # Audio players
                    st.subheader("Audio Output")

                    col_audio1, col_audio2 = st.columns(2)

                    with col_audio1:
                        st.markdown("**Voice Audio:**")
                        voice_artifact = outputs.get("voice_audio_artifact")
                        if voice_artifact and hasattr(voice_artifact, "value"):
                            # Extract the URL/path from the AudioUrlArtifact
                            audio_url = voice_artifact.value
                            if audio_url:
                                st.audio(audio_url)
                            else:
                                st.info("Voice audio artifact exists but has no URL")
                        else:
                            st.info("No voice audio available")

                    with col_audio2:
                        st.markdown("**Music Audio:**")
                        music_artifact = outputs.get("music_audio_artifact")
                        if music_artifact and hasattr(music_artifact, "value"):
                            # Extract the URL/path from the AudioUrlArtifact
                            audio_url = music_artifact.value
                            if audio_url:
                                st.audio(audio_url)
                            else:
                                st.info("Music audio artifact exists but has no URL")
                        else:
                            st.info("No music audio available")

                    # Text outputs with tabs for original vs massaged
                    st.subheader("Monologue Outputs")

                    mono_tab1, mono_tab2 = st.tabs(["Original Monologue", "Massaged for TTS"])

                    with mono_tab1:
                        st.text_area(
                            "Original speech from character:",
                            value=outputs.get("speechwriter_output", ""),
                            height=200,
                            disabled=True,
                            key="speechwriter_output_display",
                        )

                    with mono_tab2:
                        st.text_area(
                            "Acting coach's refined version for TTS:",
                            value=outputs.get("acting_coach_output", ""),
                            height=200,
                            disabled=True,
                            key="acting_coach_output_display",
                        )

                    # Retrospective
                    st.subheader("Retrospective")
                    retrospective_content = outputs.get("retrospective", "")
                    if retrospective_content:
                        st.markdown(retrospective_content)
                    else:
                        st.info("No retrospective available")


if __name__ == "__main__":
    main()
