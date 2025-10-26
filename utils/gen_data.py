from ragsql.config import get_db_connection

def init_cybersecurity_table():
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed.")
        return

    try:
        with conn.cursor() as cur:
            # สร้างตารางถ้ายังไม่มี
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cybersecurity_incidents (
                    id SERIAL PRIMARY KEY,
                    incident_name VARCHAR(255),
                    threat_actor VARCHAR(255),
                    severity VARCHAR(50),
                    affected_system TEXT,
                    attack_vector TEXT,
                    date_reported DATE
                );
            """)

            # เพิ่มข้อมูลตัวอย่าง
            incidents = [
                ("RansomLock Attack", "BlackBite Group", "High", "Windows Server 2022", "Phishing Email", "2025-01-12"),
                ("SQL Breach", "DataHunter", "Critical", "PostgreSQL Cluster", "SQL Injection", "2025-02-08"),
                ("DDoS Storm", "AnonX", "Medium", "E-commerce Web API", "Botnet", "2025-03-21"),
                ("Privilege Escalation", "Unknown", "High", "Linux Kernel 6.8", "Local Exploit", "2025-04-30"),
                ("Credential Leak", "CrimsonFox", "Low", "Corporate VPN", "Password Reuse", "2025-05-15"),
            ]

            cur.executemany("""
                INSERT INTO cybersecurity_incidents
                (incident_name, threat_actor, severity, affected_system, attack_vector, date_reported)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, incidents)

        conn.commit()
        print("Cybersecurity sample data inserted successfully.")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    init_cybersecurity_table()
