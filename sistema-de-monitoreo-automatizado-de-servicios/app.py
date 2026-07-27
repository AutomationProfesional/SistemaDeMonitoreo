from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def dashboard():
    """Renderiza el dashboard con los datos del monitoreo"""
    try:
        conn = sqlite3.connect("monitor.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Obtener el último estado de cada servicio
        cursor.execute("""
        SELECT *
        FROM logs
        WHERE id IN (
            SELECT MAX(id)
            FROM logs
            GROUP BY service               
        )
        ORDER BY id DESC
        """)

        logs = cursor.fetchall()
        conn.close()

        # Calcular estadísticas
        total = len(logs)
        up_count = sum(1 for log in logs if log['status'] == "UP")
        error_count = total - up_count

        return render_template(
            "index.html",
            logs=logs,
            total=total,
            up_count=up_count,
            error_count=error_count,
            timestamp=datetime.now().strftime("%H:%M:%S")
        )
    
    except Exception as e:
        print(f"❌ Error en dashboard: {e}")
        return f"<h1>Error</h1><p>{str(e)}</p>", 500

@app.route("/api/stats")
def api_stats():
    """Retorna estadísticas en JSON (para futuras integraciones)"""
    try:
        conn = sqlite3.connect("monitor.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM logs
        WHERE id IN (
            SELECT MAX(id)
            FROM logs
            GROUP BY service               
        )
        """)

        logs = cursor.fetchall()
        conn.close()

        total = len(logs)
        up_count = sum(1 for log in logs if log['status'] == "UP")
        error_count = total - up_count

        return {
            "total": total,
            "up_count": up_count,
            "error_count": error_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🌐 DASHBOARD FLASK INICIADO")
    print("="*50)
    print("📱 Accede a: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)