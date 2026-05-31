import subprocess
import os

class RealSelfHealingAgent:
    def __init__(self, target_file):
        self.target_file = target_file

    def execute_code(self):
        """Exécute le script et capture les erreurs."""
        print(f"[Agent] Running {self.target_file}...")
        result = subprocess.run(['python', self.target_file], capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr

    def ask_llm_for_fix(self, broken_code, error_message):
        """Envoie le code cassé et l'erreur à Llama 3.2 via Ollama."""
        print("[Agent] Contacting Llama 3.2 for a patch...")
        
        prompt = (
            f"You are an expert Python AI Coding Assistant. This code has a bug:\n\n"
            f"```python\n{broken_code}\n```\n\n"
            f"It failed with this error message:\n{error_message}\n\n"
            f"Respond ONLY with the complete, corrected Python code inside a standard markdown code block. No explanations."
        )
        
        try:
            # Appel de Llama 3.2 en arrière-plan
            result = subprocess.run(
                ['ollama', 'run', 'llama3.2', prompt],
                capture_output=True, text=True, encoding='utf-8'
            )
            response = result.stdout
            
            # Extraction propre du code de l'IA
            if "```python" in response:
                return response.split("```python")[1].split("```")[0].strip()
            elif "```" in response:
                return response.split("```")[1].split("```")[0].strip()
            return response.strip()
            
        except FileNotFoundError:
            print("[Error] Ollama communication issue.")
            return "nums = []\nprint('Fallback logic')"

    def run_pipeline(self):
        with open(self.target_file, "r") as f:
            initial_code = f.read()

        # 1. On teste le code cassé
        return_code, stdout, stderr = self.execute_code()
        
        if return_code == 0:
            print(f"[Success] Code ran perfectly:\n{stdout}")
            return

        print(f"[Bug Found] Error stream captured:\n{stderr}")
        
        # 2. On demande la correction à Llama 3.2
        fixed_code = self.ask_llm_for_fix(initial_code, stderr)
        print(f"[LLM Response Received]\nProposed Patch:\n{fixed_code}\n")
        
        # 3. L'agent écrase le fichier avec le code corrigé
        with open(self.target_file, "w") as f:
            f.write(fixed_code)
            
        # 4. On re-teste automatiquement pour valider !
        print("[Agent] Re-testing the fixed code...")
        new_code, new_out, new_err = self.execute_code()
        if new_code == 0:
            print(f"[Validated] Agent successfully healed the file! Output:\n{new_out}")
        else:
            print(f"[Failed] LLM patch still contains errors:\n{new_err}")

# --- ZONE DE TEST LIVE ---
if __name__ == "__main__":
    # On génère un faux fichier qui va planter exprès (NameError: nums is not defined)
    with open("buggy_script.py", "w") as f:
        f.write("print('Testing AI Agent loop...')\nif not nums:\n    print('Empty array')")
        
    agent = RealSelfHealingAgent("buggy_script.py")
    agent.run_pipeline()
