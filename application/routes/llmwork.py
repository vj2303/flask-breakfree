from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from application import db
from application.models import Participants, Report
from application.controllers.data_service import fetch_all_data, fetch_all_data_for_leader
from application.controllers.llm_readiness import data_for_llm, generate_readliness_analysis
from application.controllers.llm_competency import generate_competency_report
from application.controllers.llm_summary import generate_summary
from application.utils.excel import read_scores_from_excel, read_scores_from_excel_for_leader
from application.utils.word_report import generate_word_report
from application.utils.emailer import send_email
from application.utils.stats import calculate_overall_average
from application.config.settings import EXCEL_FILE_PATH1, EXCEL_FILE_PATH2, EXCEL_FILE_PATH3
# application/routes/llmwork.py (append)
from flask import request, jsonify
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

LLM = Blueprint('LLM', __name__)

#this are all excel file path for the excel data
EXCEL_FILE_PATH = r'scores/SJT_Scores_Overall_with_Competency_Scores_Batch_1_Post_Assessment.xlsx'
EXCEL_FILE_PATH1 = r'scores/excel_data_proper.xlsx'
EXCEL_FILE_PATH2 = r'scores/old_assement_score.xlsx'
EXCEL_FILE_PATH3 = r'scores/readliness_score_old_data.xlsx'

@LLM.route('/')
def index():
    return "LLM Blueprint is working!"

#this is main function to map to UI on render the HTML PAGE
@LLM.route('/report_generation', methods=['GET', 'POST'])
def report_generation():
    participants = Participants.query.all()
    leaders = set(participant.p_leader for participant in participants)
    if request.method == 'POST':
        participant_name = request.form.get('participant')
        report_type = request.form.get('reportType')
        leader_name = request.form.get('leader')
        
        
        # Check if neither a participant nor a leader is selected
        if not participant_name and not leader_name:
            flash('Please select either a Participant or a Leader.', 'danger')
            return redirect(url_for('LLM.report_generation'))
            
        if leader_name:
            if leader_name == "Visualize All":
                # Get all participants
                participants_sum = [name for name, in Participants.query.with_entities(Participants.p_name).all()]
            else:
                # Get participants for the selected leader
                participants_sum = [name for name, in Participants.query.filter_by(p_leader=leader_name).values(Participants.p_name)]

            # print(f"{participants_sum}")
            total_data = []
            all_participant_scores = []
            all_participant_scores_a = []
            all_participant_scores_r = []
            for participants in participants_sum:
                all_new_data = fetch_all_data_for_leader(participants)
                participant_scores = read_scores_from_excel_for_leader(participants, EXCEL_FILE_PATH1)
                pre_participant_scores_a = read_scores_from_excel_for_leader(participants, EXCEL_FILE_PATH2)
                pre_participant_scores_r = read_scores_from_excel_for_leader(participants, EXCEL_FILE_PATH3)
                all_participant_scores.append(participant_scores)
                all_participant_scores_a.append(pre_participant_scores_a)
                all_participant_scores_r.append(pre_participant_scores_r)
                total_data.append(all_new_data['average_scores']) # type: ignore

            overall_average_scores = calculate_overall_average(total_data)
            overall_readliness_scores = calculate_overall_average(all_participant_scores)
            overall_pre_application_scores = calculate_overall_average(all_participant_scores_a)
            overall_pre_readliness_scores = calculate_overall_average(all_participant_scores_r)
        
        all_data, participant = fetch_all_data(participant_name)
        # print(all_data)
       
        if not participant:
            pass
        
        if report_type == 'pdf':
            # print(all_data)
            if not all_data['average_scores'] :
                flash('No data found for the selected participant.', category='warning')
                return redirect(url_for('LLM.report_generation'))
            
            try:
                new_report = Report(name=participant_name, typeof='pdf', status='queued')
                db.session.add(new_report)
                db.session.commit()
                print(f"Added new report: ID={new_report.id}, Name={new_report.name}, Type={new_report.typeof}")
            except Exception as e:
                print("error")
            
            participant_scores = read_scores_from_excel(participant_name,EXCEL_FILE_PATH1)
            analysis_dict = []
            competencies = list(all_data['average_scores'].keys())
            avg_scores = list(all_data['average_scores'].values())
            readliness_score = list( participant_scores.iloc[0, 1:])
            for i in range(len(competencies)):
                analysis_dict.append({
                    'Competency': competencies[i],
                    'Readiness': readliness_score[i],
                    'Application': avg_scores[i]
                })
            analysis_dict_data = generate_readliness_analysis(analysis_dict,all_data['participant_name'].split()[0])
            # Process each competency and generate parts of the report
            final_report = []
            final_summary = []
            iteration_count = 0
            summary_data = []
            for competency_data in data_for_llm(all_data):
               if iteration_count == 4 :
                   break 
               candidate_name =  all_data['participant_name'].split()[0]
               full_report =  generate_competency_report(competency_data,candidate_name)
               final_report.append(full_report)
               summary_data.append(competency_data)
               print("we got 1st output")

            final_summary = generate_summary(summary_data, all_data['participant_name'].split()[0])
            cleaned_json = final_summary.replace('json', '')
            new_str = cleaned_json.replace('```', " ")
            new_json = json.loads(new_str)
            # final_report = "yes"

            stream = generate_word_report(final_report,  all_data['average_scores'], all_data['participant_name'], analysis_dict_data, new_json)
            document_filename = 'competency_report.docx'
            with open(document_filename, 'wb') as f:
                f.write(stream.getvalue())
        
            print(f"File saved as: {os.path.abspath(document_filename)}")
            send_email('Word Report', 'This is a test email sent from a Python script.', 'shreyas.datamango@gmail.com',document_filename)
            return send_file(stream, as_attachment=True, download_name=document_filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        flash('Report generated successfully.', category='success')

    return render_template('report_generation.html', participants=participants, user=current_user,leaders=leaders)


@LLM.route("/api/competency-report", methods=["POST"])
def api_competency_report():
    """
    Body:
    {
      "input_context": {... or [...]},  # your per-competency data block
      "candidate_name": "Alice"
    }
    Returns JSON report.
    """
    payload = request.get_json(silent=True) or {}
    input_context = payload.get("input_context")
    candidate_name = payload.get("candidate_name")

    if not input_context or not candidate_name:
        return jsonify({"error": "input_context and candidate_name are required"}), 400

    try:
        report = generate_competency_report(input_context, candidate_name)
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@LLM.route("/api/summary", methods=["POST"])
def api_summary():
    """
    Body:
    {
      "summary_data": [{"competency": "...", "application_score": 3.2, ...}, ...],
      "candidate_first_name": "Alice"
    }
    Returns JSON summary.
    """
    payload = request.get_json(silent=True) or {}
    summary_data = payload.get("summary_data")
    candidate_first_name = payload.get("candidate_first_name")

    if not isinstance(summary_data, list) or not candidate_first_name:
        return jsonify({"error": "summary_data (list) and candidate_first_name are required"}), 400

    try:
        summary = generate_summary(summary_data, candidate_first_name)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@LLM.route("/api/readiness-analysis", methods=["POST"])
def api_readiness_analysis():
    """
    Body:
    {
      "analysis_rows": [
         {"Competency": "Communication", "Readiness": 3.4, "Application": 3.1},
         ...
      ],
      "candidate_first_name": "Alice"
    }
    """
    payload = request.get_json(silent=True) or {}
    rows = payload.get("analysis_rows") or payload.get("analysis_dict")  # be flexible
    first = payload.get("candidate_first_name") or payload.get("first_name")

    if not isinstance(rows, list) or not first:
        return jsonify({"error": "analysis_rows (list) and candidate_first_name are required"}), 400

    try:
        result = generate_readliness_analysis(rows, first)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@LLM.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from LLM blueprint!"})