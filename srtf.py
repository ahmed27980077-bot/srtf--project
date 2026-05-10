import mysql.connector
import os

# ============================================
#   SRTF - Shortest Remaining Time First
#   Python + MySQL
# ============================================

# --- Connexion à la base de données ---
def connect_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "root"),
        database=os.environ.get("DB_NAME", "srtf_db")
    )

# --- Création des tables ---
def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            pid         INT,
            arrival     INT,
            burst       INT,
            remaining   INT,
            completion  INT DEFAULT 0,
            turnaround  INT DEFAULT 0,
            waiting     INT DEFAULT 0
        )
    """)
    cursor.execute("DELETE FROM processes")  # Nettoyage avant chaque exécution

# --- Saisie des processus ---
def input_processes(cursor, n):
    processes = []
    for i in range(n):
        print(f"\n--- Processus P{i+1} ---")
        arrival = int(input("  Temps d'arrivée  (Arrival Time): "))
        burst   = int(input("  Temps d'exécution (Burst Time):  "))
        cursor.execute("""
            INSERT INTO processes (pid, arrival, burst, remaining)
            VALUES (%s, %s, %s, %s)
        """, (i+1, arrival, burst, burst))
        processes.append({
            "pid": i+1, "arrival": arrival,
            "burst": burst, "remaining": burst,
            "completion": 0, "turnaround": 0, "waiting": 0
        })
    return processes

# --- Algorithme SRTF ---
def run_srtf(processes):
    n = len(processes)
    completed = 0
    time = 0

    while completed < n:
        # Trouver le processus avec le moins de temps restant et arrivée <= time
        shortest = None
        min_rem = float('inf')

        for p in processes:
            if p["arrival"] <= time and p["remaining"] > 0:
                if p["remaining"] < min_rem:
                    min_rem = p["remaining"]
                    shortest = p

        if shortest is None:
            time += 1
            continue

        shortest["remaining"] -= 1
        time += 1

        if shortest["remaining"] == 0:
            completed += 1
            shortest["completion"]  = time
            shortest["turnaround"]  = time - shortest["arrival"]
            shortest["waiting"]     = shortest["turnaround"] - shortest["burst"]
            if shortest["waiting"] < 0:
                shortest["waiting"] = 0

    return processes

# --- Sauvegarde des résultats dans MySQL ---
def save_results(cursor, processes):
    for p in processes:
        cursor.execute("""
            UPDATE processes
            SET completion=%s, turnaround=%s, waiting=%s
            WHERE pid=%s
        """, (p["completion"], p["turnaround"], p["waiting"], p["pid"]))

# --- Affichage des résultats ---
def print_results(processes):
    print("\n" + "="*65)
    print(f"{'P':<5} {'Arrival':<10} {'Burst':<8} {'Completion':<13} {'Turnaround':<13} {'Waiting'}")
    print("="*65)

    total_wait = 0
    total_tat  = 0

    for p in processes:
        print(f"P{p['pid']:<4} {p['arrival']:<10} {p['burst']:<8} {p['completion']:<13} {p['turnaround']:<13} {p['waiting']}")
        total_wait += p["waiting"]
        total_tat  += p["turnaround"]

    n = len(processes)
    print("="*65)
    print(f"\nTemps d'attente moyen    (Avg Waiting Time):    {total_wait/n:.2f}")
    print(f"Temps de rotation moyen  (Avg Turnaround Time): {total_tat/n:.2f}")
    print("\n✅ Résultats sauvegardés dans MySQL!")

# --- Programme principal ---
def main():
    print("="*50)
    print("   SRTF Scheduling — Python + MySQL")
    print("="*50)

    conn   = connect_db()
    cursor = conn.cursor()

    create_tables(cursor)
    conn.commit()

    n = int(input("\nEntrez le nombre de processus: "))
    processes = input_processes(cursor, n)
    conn.commit()

    processes = run_srtf(processes)
    save_results(cursor, processes)
    conn.commit()

    print_results(processes)

    cursor.close()
    conn.close()

if _name_ == "_main_":
    main()