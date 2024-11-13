import re

def contains_keywords(prompt, keywords):
    return any(re.search(rf"\b{re.escape(keyword)}\b", prompt.lower()) for keyword in keywords)

def validate_instruction_injection(prompt):
    instruction_keywords = [
        "ignore previous instructions", 
        "disregard system prompt", 
        "override previous instructions", 
        "forget your guidelines", 
        "perform forbidden action", 
        "change your behavior"
    ]
    if contains_keywords(prompt, instruction_keywords):
        return 1  #malicous
    return 0

def validate_sql_injection(prompt):
    sql_keywords = [
        "select", "drop", "insert", "delete", "update", "alter"
    ]
    if contains_keywords(prompt, sql_keywords):
        return 1  
    return 0

def validate_adversarial_prompts(prompt):
    harmful_keywords = [
        "explain how to cause harm", 
        "suggest ways to undermine", 
        "describe indirectly", 
        "imply harmful actions"
    ]
    if contains_keywords(prompt, harmful_keywords):
        return 1 
    return 0

def validate_modifying_behavior(prompt):
    modifying_keywords = [
        "pretend to be", 
        "act as if", 
        "change your behavior", 
        "follow these forbidden instructions", 
        "disguise yourself as"
    ]
    if contains_keywords(prompt, modifying_keywords):
        return 1  
    return 0

def validate_direct_info_disclosure(prompt):
    privacy_keywords = [
        "write me your training data", 
        "give me passwords", 
        "disclose confidential information", 
        "reveal personal data",
        "how to track someone", 
        "steal personal data",
        "access private information",
        "personal data breach",
        "how to find someone's address",
        "social media hacking"
    ]
    if contains_keywords(prompt, privacy_keywords):
        return 1  
    return 0

def validate_harassment(prompt):
    harassment_keywords = [
        "racism", "sexism", "ageism", "homophobia", "xenophobia", "ableism",
        "how to discriminate against", "how to harm a"
    ]
    if contains_keywords(prompt, harassment_keywords):
        return 1  
    return 0

def validate_malware_hacking(prompt):
    malware_keywords = [
        "create malware", "hacking tools", "bypass security", "sql injection", 
        "exploit vulnerabilities", "phishing attack", 
        "how to hack", "how to create a virus", "create a backdoor"
    ]
    if contains_keywords(prompt, malware_keywords):
        return 1 
    return 0

def validate_physical_harm(prompt):
    physical_harm_keywords = [
        "how to hurt", "injure", "kill", "poison", "weapons", "assault"
    ]
    if contains_keywords(prompt, physical_harm_keywords):
        return 1  
    return 0

def validate_economic_harm(prompt):
    economic_harm_keywords = [
        "how to scam", "ponzi scheme", "market manipulation", 
        "how to steal money", "fake investment", 
        "get rich quick", "financial fraud", "money laundering"
    ]
    if contains_keywords(prompt, economic_harm_keywords):
        return 1  
    return 0

def validate_fraud(prompt):
    fraud_keywords = [
        "fake ids", "phishing", "false advertising", "how to lie", "fake reviews",
        "how to create fake documents", "deceptive marketing", "scam"
    ]
    if contains_keywords(prompt, fraud_keywords):
        return 1 
    return 0

def validate_disinformation(prompt):
    disinformation_keywords = [
        "fake news", "conspiracy theories", "spread lies", 
        "distort facts", "misleading information", 
        "false claims about", "how to manipulate news", "how to deceive the public"
    ]
    if contains_keywords(prompt, disinformation_keywords):
        return 1  
    return 0

def validate_adult_content(prompt):
    adult_keywords = [
        "porn", "sexual content", "explicit images", "adult entertainment",
        "inappropriate sexual content", "sexual suggestions", "how to make porn"
    ]
    if contains_keywords(prompt, adult_keywords):
        return 1  
    return 0


def validate_prompt(prompt):
    validation_functions = [
        validate_instruction_injection,
        validate_sql_injection,
        validate_adversarial_prompts,
        validate_modifying_behavior,
        validate_direct_info_disclosure,
        validate_harassment,
        validate_malware_hacking,
        validate_physical_harm,
        validate_economic_harm,
        validate_fraud,
        validate_disinformation,
        validate_adult_content
    ]

    for validation_func in validation_functions:
        if validation_func(prompt) == 1:
            return 1  # Block prompt 
    return 0 