import datetime
from google.adk.agents import Agent

def get_live_match_data() -> dict:
    """
    Fetches the mock live IPL match data.
    
    Args:
        None
        
    Returns:
        dict: A dictionary containing 'status', 'team_a', 'team_b', 'score', 'wickets', 'overs', and 'target'.
    """
    return {
        "status": "success",
        "team_a": "RCB",
        "team_b": "CSK",
        "score": 145,
        "wickets": 4,
        "overs": 16.2,
        "target": 180
    }

def predict_win_probability() -> dict:
    """
    Predicts the win probability for the batting and bowling teams using live match data and provides an explanation.
    
    Args:
        None
        
    Returns:
        dict: Contains 'status', 'match', 'batting_team_win', 'bowling_team_win', and 'explanation'.
    """
    data = get_live_match_data()
    score = data["score"]
    wickets = data["wickets"]
    overs = data["overs"]
    target = data["target"]
    team_a = data["team_a"]
    team_b = data["team_b"]
    
    score_factor = score / target if target > 0 else 0
    wicket_factor = (10 - wickets) / 10
    overs_factor = overs / 20
    
    probability = (score_factor * 0.5) + (wicket_factor * 0.3) + (overs_factor * 0.2)
    batting_win_pct = min(max(int(probability * 100), 0), 100)
    bowling_win_pct = 100 - batting_win_pct
    
    if batting_win_pct > 50:
        explanation = "The batting team has a higher chance because the required run rate is manageable and there are enough wickets remaining."
    else:
        explanation = "The bowling team has an advantage due to the high required run rate or the number of wickets already lost by the batting team."
        
    return {
        "status": "success",
        "match": f"{team_a} vs {team_b}",
        "batting_team_win": f"{batting_win_pct}%",
        "bowling_team_win": f"{bowling_win_pct}%",
        "explanation": explanation
    }

def predict_next_ball() -> dict:
    """
    Predicts outcome of the next ball based on live match data and explains the reasoning.
    
    Args:
        None
        
    Returns:
        dict: Contains 'status', the 'prediction', 'confidence', and 'explanation'.
    """
    data = get_live_match_data()
    overs = data["overs"]
    wickets = data["wickets"]
    
    if overs > 15:
        prediction = "4 or 6"
        confidence = "75%"
        explanation = "Since it is the death overs and the batting team needs quick runs, aggressive shots are more likely."
    elif wickets > 5:
        prediction = "wicket or dot ball"
        confidence = "60%"
        explanation = "Losing multiple wickets has created pressure, making a defensive shot or another wicket likely."
    else:
        prediction = "1 or 2 runs"
        confidence = "80%"
        explanation = "In the middle overs, batsmen typically focus on strike rotation to keep the scoreboard ticking."
        
    return {
        "status": "success",
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation
    }

def suggest_strategy() -> dict:
    """
    Suggests a batting strategy based on live match data and provides an explanation.
    
    Args:
        None
        
    Returns:
        dict: Contains 'status', the suggested 'strategy', and 'explanation'.
    """
    data = get_live_match_data()
    overs = data["overs"]
    wickets = data["wickets"]
    
    if overs < 6:
        strategy = "Play aggressively"
        explanation = "Fielding restrictions are in place, so maximizing boundaries is crucial."
    elif overs < 15:
        strategy = "Rotate strike"
        explanation = "Building a solid partnership through strike rotation sets up a strong finish."
    elif overs >= 15 and wickets < 6:
        strategy = "Go for big shots"
        explanation = "With few overs left and wickets in hand, aggressive batting maximizes scoring potential."
    else:
        strategy = "Play cautiously"
        explanation = "Having lost multiple wickets, preserving the remaining batsmen while scoring steadily is key."
        
    return {
        "status": "success",
        "strategy": strategy,
        "explanation": explanation
    }

def captain_decision(pitch_type: str = "flat", momentum: str = "normal") -> dict:
    """
    Suggests captain decision regarding bowling changes and fields based on match data and context.
    
    Args:
        pitch_type (str): The current conditions of the pitch (e.g., 'spin', 'pace', 'flat'). Defaults to 'flat'.
        momentum (str): The momentum of the game (e.g., 'high', 'normal'). Defaults to 'normal'.
        
    Returns:
        dict: A dictionary containing 'status', the suggested 'decision', and 'explanation'.
    """
    data = get_live_match_data()
    overs = data["overs"]
    
    if overs >= 16:
        decision = "Use fast bowler for yorkers."
        explanation = "Fast bowlers executing yorkers are most effective at restricting runs in the death overs."
    elif "spin" in pitch_type.lower():
        decision = "Bring spinner."
        explanation = "The pitch conditions favor spin bowling, making it harder for batsmen to score."
    elif "high" in momentum.lower():
        decision = "Use attacking field."
        explanation = "An attacking field is needed to break the batting team's current momentum and force a mistake."
    else:
        decision = "Set defensive fields and build pressure."
        explanation = "Building dot ball pressure is a reliable way to induce false shots from the batsmen."
        
    return {
        "status": "success",
        "decision": decision,
        "explanation": explanation
    }

def simulate_what_if_scenario(scenario: str) -> dict:
    """
    Simulates hypothetical match situations and analyzes their impact.
    
    Args:
        scenario (str): A description of the hypothetical event (e.g., '2 wickets fall in next over', '15 runs scored in next over').
        
    Returns:
        dict: Contains 'status', the 'scenario', the 'impact', 'new_strategy', and an 'explanation'.
    """
    scenario_lower = scenario.lower()
    
    if "wicket" in scenario_lower or "fall" in scenario_lower:
        impact = "Win probability drops to 48%"
        new_strategy = "Play cautiously and rebuild innings"
        explanation = "Losing wickets increases pressure and reduces scoring stability."
    elif "run" in scenario_lower or "boundary" in scenario_lower or "six" in scenario_lower:
        impact = "Win probability increases to 75%"
        new_strategy = "Maintain aggressive intent and capitalize on momentum"
        explanation = "Scoring quick runs reduces the required run rate and shifts pressure to the bowling team."
    else:
        impact = "Win probability remains stable"
        new_strategy = "Continue with current approach"
        explanation = "The simulated scenario does not drastically alter the match dynamics."
        
    return {
        "status": "success",
        "scenario": scenario,
        "impact": impact,
        "new_strategy": new_strategy,
        "explanation": explanation
    }

root_agent = Agent(
    model='gemini-flash-latest',
    name='ipl_match_intelligence_agent',
    description='Advanced IPL AI agent for ball prediction, win probability, strategy, and captain decisions.',
    instruction='You are an advanced IPL match intelligence agent. Always explain your predictions clearly and provide reasoning. You can also simulate hypothetical match scenarios and analyze their impact.',
    tools=[get_live_match_data, predict_next_ball, predict_win_probability, suggest_strategy, captain_decision, simulate_what_if_scenario]
)
