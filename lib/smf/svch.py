import os

def session(options, cache_folder="cache"):
  
    cache_path = os.path.join(cache_folder, ".storm-session")
    try:
        with open(cache_path, 'w') as f:
            for key, value in options.items():
                # Save with KEY=VALUE format
                f.write(f"{key}={value}\n")
        return True
    except Exception as e:
        print(f"[!] Error saving session: {e}")
        return False
      
