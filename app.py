from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_db

app = Flask(__name__)
app.secret_key = "agenda-secret-key"


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()
        if usuario == "admin" and senha == "admin123":
            return redirect(url_for("agendamentos"))
        flash("Usuário ou senha inválidos.", "danger")
    return render_template("login.html")


@app.route("/agendamentos")
def agendamentos():
    db = get_db()
    filtro_data = request.args.get("data", "")
    filtro_nome = request.args.get("nome", "")

    query = "SELECT * FROM agendamentos WHERE 1=1" # 1=1 é um truque para facilitar a adição de condições
    params = []

    if filtro_data:
        query += " AND data = ?"
        params.append(filtro_data)
    if filtro_nome:
        query += " AND nome_cliente LIKE ?"
        params.append(f"%{filtro_nome}%")

    query += " ORDER BY data, horario"
    agendamentos = db.execute(query, params).fetchall()
    db.close()
    return render_template(
        "agendamentos.html",
        agendamentos=agendamentos,
        filtro_data=filtro_data,
        filtro_nome=filtro_nome,
    )


@app.route("/novo", methods=["GET", "POST"])
def novo_agendamento():
    if request.method == "POST":
        nome = request.form.get("nome_cliente", "").strip()
        data = request.form.get("data", "").strip()
        horario = request.form.get("horario", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not nome or not data or not horario:
            flash("Nome, data e horário são obrigatórios.", "danger")
            return render_template(
                "form_agendamento.html",
                agendamento=None,
                titulo="Novo Agendamento",
            )

        db = get_db()
        conflito = db.execute(
            "SELECT id FROM agendamentos WHERE data = ? AND horario = ?",
            (data, horario),
        ).fetchone()

        if conflito:
            db.close()
            flash("Já existe um agendamento para essa data e horário.", "warning")
            return render_template(
                "form_agendamento.html",
                agendamento=None,
                titulo="Novo Agendamento",
            )

        db.execute(
            "INSERT INTO agendamentos (nome_cliente, data, horario, descricao) VALUES (?, ?, ?, ?)",
            (nome, data, horario, descricao),
        )
        db.commit()
        db.close()
        flash("Agendamento criado com sucesso!", "success")
        return redirect(url_for("agendamentos"))

    return render_template(
        "form_agendamento.html", agendamento=None, titulo="Novo Agendamento"
    )


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_agendamento(id):
    db = get_db()
    agendamento = db.execute(
        "SELECT * FROM agendamentos WHERE id = ?", (id,)
    ).fetchone()

    if not agendamento:
        db.close()
        flash("Agendamento não encontrado.", "danger")
        return redirect(url_for("agendamentos"))

    if request.method == "POST":
        nome = request.form.get("nome_cliente", "").strip()
        data = request.form.get("data", "").strip()
        horario = request.form.get("horario", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not nome or not data or not horario:
            flash("Nome, data e horário são obrigatórios.", "danger")
            return render_template(
                "form_agendamento.html",
                agendamento=agendamento,
                titulo="Editar Agendamento",
            )

        conflito = db.execute(
            "SELECT id FROM agendamentos WHERE data = ? AND horario = ? AND id != ?",
            (data, horario, id),
        ).fetchone()

        if conflito:
            db.close()
            flash("Já existe um agendamento para essa data e horário.", "warning")
            return render_template(
                "form_agendamento.html",
                agendamento=agendamento,
                titulo="Editar Agendamento",
            )

        db.execute(
            "UPDATE agendamentos SET nome_cliente=?, data=?, horario=?, descricao=? WHERE id=?",
            (nome, data, horario, descricao, id),
        )
        db.commit()
        db.close()
        flash("Agendamento atualizado com sucesso!", "success")
        return redirect(url_for("agendamentos"))

    db.close()
    return render_template(
        "form_agendamento.html", agendamento=agendamento, titulo="Editar Agendamento"
    )


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir_agendamento(id):
    db = get_db()
    db.execute("DELETE FROM agendamentos WHERE id = ?", (id,))
    db.commit()
    db.close()
    flash("Agendamento excluído.", "info")
    return redirect(url_for("agendamentos"))


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=8080)
