import subprocess
import os

class SelfHealingAgent:
    def __init__(self, target_file):
        self.target_file = target_file

    def execute_code(self):
        """Exécute le fichier cible et capture les erreurs de terminal."""
        print(f"[Agent] Attempting to run {self.target_file}...")
        result = subprocess.run(['python', self.target_file], capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr

    def simulate_llm_fix(self, error_message):
        """Simule la réflexion d'un LLM pour corriger une erreur spécifique."""
        print(f"[LLM Agent] Analyzing error: {error_message.strip()}")
        
        if "NameError" in error_message:
            print("[LLM Agent] Decision: Undefined variable detected. Generating fix...")
            return "nums = [1, 2, 3]\nif not nums:\n    print('Empty')\nelse:\n    print('Success: Array has elements!')"
        return "# Unresolved error"

    def run_pipeline(self):
        # 1. Première tentative d'exécution
        return_code, stdout, stderr = self.execute_code()
        
        if return_code == 0:
            print(f"[Success] Code ran perfectly:\n{stdout}")
            return

        print(f"[Bug Detected] Code failed with exit code {return_code}")
        
        # 2. Boucle de rétroaction (Feedback Loop) : On envoie l'erreur au LLM Simulation
        fixed_code = self.simulate_llm_fix(stderr)
        
        # 3. L'agent applique le correctif sur le fichier automatiquement (Self-Healing)
        print(f"[Agent] Rewriting {self.target_file} with the AI fix...")
        with open(self.target_file, "w") as f:
            f.write(fixed_code)
            
        # 4. Deuxième tentative de validation
        print("[Agent] Re-testing the fixed code...")
        new_code, new_out, new_err = self.execute_code()
        if new_code == 0:
            print(f"[Validated] Agent successfully fixed the bug! Output:\n{new_out}")
        else:
            print("[Failed] AI fix was insufficient.")

# --- SCRIPT DE TEST ---
if __name__ == "__main__":
    # On crée un fichier temporaire contenant un bug d'indentation/variable (NameError)
    broken_code = "if not nums:\n    print('Error line')"
    with open("broken_script.py", "w") as f:
        f.write(broken_code)
        
    # On lance notre agent autonome dessus
    agent = SelfHealingAgent("broken_script.py")
    agent.run_pipeline()
    
    # Nettoyage
    if os.path.exists("broken_script.py"):
        os.remove("broken_script.py")
