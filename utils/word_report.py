import json
import re 
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from docx import Document 
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement, ns
from docx.oxml import OxmlElement, ns
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from application.utils.excel import read_scores_from_excel

EXCEL_FILE_PATH = r'applications/SJT_Scores_Overall_with_Competency_Scores_Batch_1_Post_Assessment.xlsx'
EXCEL_FILE_PATH1 = r'applications/excel_data_proper.xlsx'
EXCEL_FILE_PATH2 = r'applications/old_assement_score.xlsx'
EXCEL_FILE_PATH3 = r'applications/readliness_score_old_data.xlsx'

def generate_introduction_text(participant_name):
    introduction_text = f'''
Hi {participant_name},

Congratulations on having completed the Katalyst – A Leadership Development Intervention.

Your journey through this program has been one of growth, reflection, and development. Over the past months, you've engaged in a series of activities designed to assess and enhance your leadership competencies. These competencies, aligned with our organization's framework, are vital for success in your current role and future leadership positions.

Enclosed is your final report, which provides a comprehensive overview of your performance and development areas identified during the program. This report offers valuable insights into your strengths and areas for growth, empowering you to continue your development journey.

In addition to the assessments, you also participated in a six-month learning journey, which included a series of training programs and coaching sessions with a dedicated executive coach. These experiences have complemented the assessments, providing you with a holistic approach to your development as a leader.

As you review your final report, remember that it's not just about the results but about the journey and the lessons learned along the way. We encourage you to reflect on your achievements and use the feedback provided to drive your ongoing growth and success.

If you have any questions or need further support, please don't hesitate to reach out to our Human Resource team.

Once again, congratulations on your accomplishments, and we wish you continued success in your leadership journey.
    '''
    return introduction_text


def readliness_text(participant_name):
    
    introduction_text = f'''
    Readiness assessment evaluates a participant's intellectual knowledge and their ability to apply competencies, measuring whether they can correctly identify the most appropriate actions in various situations. Typically, participants report their readiness through a psychometric instrument.
    
    Application assessment, on the other hand, focuses on a participant's capacity to demonstrate the desired competencies in real work-related situations. This evaluation involves observers assessing the participant's performance in simulated activities.
    
    Ideally, one would aim for a close alignment between readiness and application. When readiness exceeds application, it suggests that a person has the knowledge of what needs to be done but may struggle to effectively apply or display these behaviors in real-life interactions and situations. To address this, individuals may need to practice these behaviors and receive ongoing coaching and feedback.
    
    Conversely, when application surpasses readiness, it indicates that an individual naturally demonstrates these competencies but may not be consciously aware of how they do so. In this case, the focus may shift towards developing a deeper understanding through awareness training that covers models, theories, and approaches, helping the individual practice these competencies with more deliberate thoughtfulness.
    '''
    return introduction_text

#for setting a proper table border
def set_cell_borders(cell, **borders):
    tc_pr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for key, value in borders.items():
        border = OxmlElement(f'w:{key}')
        border.set(ns.qn('w:val'), value['val'])
        border.set(ns.qn('w:sz'), str(value['sz']))
        border.set(ns.qn('w:color'), value['color'])
        tcBorders.append(border)
    tc_pr.append(tcBorders)

#for giving background color to table body cells
def set_cell_background(cell, fill_color, text_color=RGBColor(255, 255, 255)):
    """ Set the background color of a cell and adjust the text color directly for each run. """
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(ns.qn('w:fill'), fill_color)
    cell._tc.get_or_add_tcPr().append(shading_elm)
    # Ensure that every run in the cell paragraphs is formatted correctly
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb = text_color

# for adding the text style of the whole document
def configure_styles(document):
    """ Configures document-wide styles for Arial font and specific sizes for headings and body text. """
    style = document.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(10)

    # Heading 1 Style
    heading1 = document.styles.add_style('Heading1', WD_STYLE_TYPE.PARAGRAPH)
    heading1.font.name = 'Arial'
    heading1.font.size = Pt(18)
    heading1.font.bold = True

    # Heading 2 Style
    heading2 = document.styles.add_style('Heading2', WD_STYLE_TYPE.PARAGRAPH)
    heading2.font.name = 'Arial'
    heading2.font.size = Pt(14)
    heading2.font.bold = True

    # Heading 3 Style
    heading2 = document.styles.add_style('Heading3', WD_STYLE_TYPE.PARAGRAPH)
    heading2.font.name = 'Arial'
    heading2.font.size = Pt(10)
    heading2.font.bold = True

def add_section(document, title, content_list):
    # Add section title as a heading
    document.add_heading(title, level=1)
    
    for content in content_list:
        # Split the content into descriptor and summary
        descriptor, summary = content.split(':')
        descriptor = descriptor.strip()
        summary = summary.strip()

        # Add descriptor in bold
        para = document.add_paragraph()
        run = para.add_run(descriptor + ':')
        run.bold = True
        run.font.size = Pt(12)

        # Add summary
        para = document.add_paragraph(summary)
        para.paragraph_format.left_indent = Pt(36)  # Indent summary for clarity

    # Add space after section
    document.add_paragraph()

#this function for the adding the tables in the document
def add_custom_table(document, headers, rows_data):
    """ Add a styled custom table with specified headers and data rows to the document. """
    table = document.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        set_cell_background(cell, '366092')  # Blue background
        cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Add data rows with bullet points and format text
    for row_data in rows_data:
        row = table.add_row().cells
        for i, item in enumerate(row_data):
            row[i].text = f'• {item}'  # Add bullet points to each item
            row[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

#to add the page no at the end of the page in word document
def create_footer_with_page_numbers(section):
    footer = section.footer
    footer_paragraph = footer.paragraphs[0]
    footer_paragraph.text = "Page "
    run = footer_paragraph.add_run()
    field_code = 'PAGE'
    run._r.append(OxmlElement('w:fldSimple', {qn('w:instr'): f"{field_code}"}))
    footer_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

# Function to parse the comments from a given string input
def parse_comments(input_string):
    # Extract the comments part
    comments_part = re.search(r'\["(.+?)"\]', input_string, re.DOTALL)
    if not comments_part:
        return []
    
    comments = comments_part.group(0).strip('[]"').split('",')
    comments = [comment.strip().strip('"') for comment in comments if comment.strip()]
    return comments

def set_text_color(cell, color):
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb = color

#function for the creating word document
def generate_word_report(llm_report, average_scores, participant_name, analysis_dict_data, final_summary):

    document = Document()
    configure_styles(document)
     # Apply header image to all sections
    for section in document.sections:
        # set_header_with_image(section, image_path = "C:\\Users\\chinmay\\Videos\\codes\\python\\flask_web_app_pass_u\\applications\\static\\images\\1245780.png")
        create_footer_with_page_numbers(section)

    
    document.add_heading(f'Competency Report: {participant_name}', level=0)

    # Add Introduction
    document.add_heading('Introduction', level=1 )
    candidate_name =  participant_name.split()[0]
    introduction_text = generate_introduction_text(candidate_name)

    # Split the introduction text into paragraphs where there are two new lines, and add them to the document
    for paragraph in introduction_text.strip().split('\n\n'):
        if paragraph:
            document.add_paragraph(paragraph, style='BodyText')
            document.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        else:
            document.add_paragraph('')
            document.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

     # Add First Custom Table after Introduction
    document.add_page_break()
    first_table_headers = ["DELIGHTING CUSTOMERS: SOLUTIONS & EXPERIENCE CREATOR", "BOLDLY INNOVATE: CATALYST", "OWN IT: BUSINESS LEADER", "PRIORITISE: SENSE MAKER"]
    first_rows_data = [
        ["Shares & Translates Market Insights", "Brings Perspective & Teaches", "Deep Business Knowledge", "Explains Purpose & Why"],
        ["Creates Plans to Deliver Differentiated Customer Experiences", "Multiple Sources of Input", "Enterprise Mindset", "Sets Team Objectives"],
        ["Connects Teams with Shared Customer Goals to Deliver", "Strategically resolves everyday business challenges", "Calculated Risk Taking", "Priority Management"],
        ["Sets up an engagement plan, collaborates with stakeholders, and aligns with their expectations to meet their needs.", "Iterates for Best Outcomes - by leveraging internal data and external market insight", "Proactive Decision Making", "Cross-Functional Alignment"]
    ]
    document.add_heading('Competency Overview', level=2)
    add_custom_table(document, first_table_headers, first_rows_data)

    # Add Second Custom Table
    second_table_headers = ["CONVERSING IN DIFFICULT SITUATION", "COMMUNICATING ASSERTIVELY", "LEADING WITH STRATEGY", "INSPIRING PEOPLE: TALENT CULTIVATOR"]
    second_rows_data = [
        ["Correctly identifies when and why a conversation is difficult and what role opinions, emotions, and stakes are at play in such situations.", "Expresses thoughts, feelings, and beliefs directly and appropriately", "Able to fulfil short-term expectations and also focus deeply on defining the future agenda", "Positive Authenticity & Courage"],
        ["Able to turn difficult conversations into action and results", "Shares opinions and acknowledges others' views", "Ensures alignment with overall strategies", "Talent Planning & Diverse, Strong Pipelines"],
        ["Able to translate technical and functional complexities into plans and execution", "Courageously says no and handles agreements and disagreements gracefully", "Recognizes emerging patterns and trends", "Identifies talent within and outside the organization leveraging strong networks"],
        ["Deescalates emotionally charged situations through effective use of communication.", "Possesses well-defined, experience-based ideas and articulates them confidently", "Able to allocate scarce resources wisely and channelize the collective effort of the team effectively.", "Nurtures and develops talent (within and outside the team e.g., at the college/ institute level)"]
    ]
    document.add_heading('Advanced Competency Details', level=2)
    add_custom_table(document, second_table_headers, second_rows_data)

    # Add Competency Summary section
    document.add_page_break()
    document.add_heading('Competency Summary', level=1)

    # Sort the competencies by average score in descending order
    sorted_competencies = sorted(average_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Add Top Competencies section
    paragraph = document.add_paragraph('TOP COMPETENCIES', style='Heading 2')
    top_competencies = sorted_competencies[:3]
    # print(top_competencies)
    for competency, score in top_competencies:
        document.add_paragraph(f'{competency}')# convert it into lines 

    # Add Areas of Potential Strength section
    paragraph = document.add_paragraph('AREAS OF POTENTIAL STRENGTH', style='Heading 2')
    potential_strengths = sorted_competencies[3:5]
    for competency, score in potential_strengths:
        document.add_paragraph(f'{competency}')# convert it into lines 
        
    # Add Areas of Development section
    paragraph = document.add_paragraph('AREAS OF DEVELOPMENT', style='Heading 2')
    areas_of_development = sorted_competencies[5:]
    for competency, score in areas_of_development[:3]:
        document.add_paragraph(f'{competency}')# convert it into lines 

   # Add LLM report text
    document.add_page_break()

    # Iterate through each JSON string in the list
    for json_string in llm_report:
        # Load the JSON data
        json_data = json.loads(json_string)
        # Iterate through the top-level keys
        for section, content in json_data.items():
            # Add section title
            document.add_heading(section, level=1)
            # Add pie chart for the section if it is in average_scores
            if section in average_scores:
                avg_score = average_scores[section]
                avg_score = round(avg_score) if avg_score >= 2.5 else int(avg_score)
                sizes = [avg_score, 3 - avg_score]  # Adjust accordingly
                colors = ['skyblue', 'lightgray']  # The colors for the pie slices

                fig, ax = plt.subplots(figsize=(3, 3))  # Set the figure size to 3cm x 3cm
                ax.pie(sizes, colors=colors, radius=1, startangle=90)  # Draw the pie chart

                # Add a white circle in the center to create a donut look
                center_circle = plt.Circle((0, 0), 0.7, color='white')  # type: ignore # Create a white circle with radius 0.7
                ax.add_artist(center_circle)  # Add the circle to the pie chart

                # Ensure the pie chart is circular and remove labels/tick marks
                ax.set_title('', fontsize=16)  # Set an empty title
                ax.axis('equal')  # Ensure the pie chart is circular
                plt.setp(ax.get_xticklabels(), visible=False)  # Hide the x-axis tick labels
                plt.setp(ax.get_yticklabels(), visible=False)  # Hide the y-axis tick labels

                # Save plot to a BytesIO object
                img_stream = BytesIO()
                plt.savefig(img_stream, format='png')
                img_stream.seek(0)  # rewind the data

                plt.close(fig)  # Close the plot to free up resources

                # Add the pie chart to the documentument
                document.add_picture(img_stream, width=Inches(1.0))
                document.add_paragraph(f'Figure: Score Distribution for {section}')
        
                # Iterate through the sub-sections
                for subsection, details in content.items():
                    # Add subsection title
                    document.add_heading(subsection, level=2)
                    
                    # Iterate through the details
                    for detail_title, detail_content in details.items():
                        # Add detail title and content
                        document.add_heading(detail_title, level=3)
                        document.add_paragraph(detail_content)
                
                # Add a page break after each competency
                document.add_page_break()
             
    # Add LLM summary report text
    # document.add_page_break()
  
    document.add_heading('Overall Summary of Feedback', level=1)
    # Add the new function to add data to the document
    def add_data_to_document(data, title):
        document.add_heading(title, 0)
        for descriptor_name, summary in data.items():
            document.add_heading(f"{descriptor_name}", level=2)
            document.add_paragraph(summary, style="List Bullet")

    # Add strengths to the document
    add_data_to_document(final_summary["Strengths"], "Strengths")
    # Add areas of opportunity to the document
    add_data_to_document(final_summary["Areas of Opportunity"], "Areas of Opportunity")

    document.add_page_break()

    # Insert new section "Readiness Vs. Application"
    document.add_heading('Readiness Vs. Application', level=1)

    # How to read this information section
    document.add_heading('How to read this information', level=2)
    readiness_vs_application_text = """
Readiness assessment evaluates a participant's intellectual knowledge and their ability to apply competencies, measuring whether they can correctly identify the most appropriate actions in various situations. Typically, participants report their readiness through a psychometric instrument.

Application assessment, on the other hand, focuses on a participant's capacity to demonstrate the desired competencies in real work-related situations. This evaluation involves observers assessing the participant's performance in simulated activities.

Ideally, one would aim for a close alignment between readiness and application. When readiness exceeds application, it suggests that a person has the knowledge of what needs to be done but may struggle to effectively apply or display these behaviors in real-life interactions and situations. To address this, individuals may need to practice these behaviors and receive ongoing coaching and feedback.

Conversely, when application surpasses readiness, it indicates that an individual naturally demonstrates these competencies but may not be consciously aware of how they do so. In this case, the focus may shift towards developing a deeper understanding through awareness training that covers models, theories, and approaches, helping the individual practice these competencies with more deliberate thoughtfulness.
    """
    document.add_paragraph(readiness_vs_application_text, style='BodyText')

    # Continue with Competency Analysis Visualization

    participant_scores = read_scores_from_excel(participant_name,EXCEL_FILE_PATH1)
    pre_scores = read_scores_from_excel(participant_name, EXCEL_FILE_PATH2)
    pre_readliness_score = read_scores_from_excel(participant_name ,  EXCEL_FILE_PATH3)
    competencies = list(average_scores.keys())
    avg_scores = list(average_scores.values())

    # print(participant_scores)
    df_pre_scores = pd.DataFrame({'Competency': competencies, 'PRE_SCORE': pre_scores.iloc[0, 1:]})
    df_pre_readliness_score = pd.DataFrame({'Competency': competencies, 'PRE_SCORE_READLINESS': pre_readliness_score.iloc[0, 1:]})
   
    # Create DataFrames for visualization
    df_avg_scores = pd.DataFrame({'Competency': competencies, 'Average Score': avg_scores})
    df_participant_scores = pd.DataFrame({'Competency': competencies, 'SJIT Score': participant_scores.iloc[0, 1:]})
   
    # Merge the DataFrames on 'Competency'
    df_visualize = pd.merge(df_avg_scores, df_participant_scores, on='Competency')

    sns.set_style("white")
    plt.figure(figsize=(10,6))
    ax = sns.lineplot(data=df_visualize, x='Competency', y='Average Score', marker='o', color='skyblue', linewidth=2.5, label='Application Score')
    sns.lineplot(data=df_visualize, x='Competency', y='SJIT Score', marker='o', color='green', linewidth=2.5, label='Readiness Score')
    # Adding text labels on the plot lines
    for x, y in zip(df_visualize['Competency'], df_visualize['Average Score']):
        plt.text(x, y, f'{y:.2f}', color='blue', ha='right', va='bottom')
    for x, y in zip(df_visualize['Competency'], df_visualize['SJIT Score']):
        plt.text(x, y, f'{y:.2f}', color='green', ha='right', va='bottom')
    title = (f'Average Scores of Competency - {candidate_name}')
    plt.title(title)
    plt.xlabel('Competency')
    plt.ylabel('Score')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()

    # Save plot to a BytesIO object
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)  # rewind the data
    plt.close()  # Close the plot to free up resources

    # Add the plot to the document
    document.add_picture(img_stream, width=Inches(5.0))
    diagram_define = ('Figure 1: Competency Score Analysis')
    document.add_paragraph(diagram_define)

    # Create a table with the required columns
    table = document.add_table(rows=1, cols=4)
    table.style = 'TableGrid'

    # Set column widths
    table.columns[0].width = Inches(1.5)  # Competency
    table.columns[1].width = Inches(1.0)  # Application Average
    table.columns[2].width = Inches(1.0)  # Readiness
    table.columns[3].width = Inches(2.5)  # Analysis

    # Set column names with centered text and blue background
    headers = ["Competency", "Application Average", "Readiness", "Analysis"]
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        cell.paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, '#008080')  # Light blue color

    # Add data rows
    competencies = list(average_scores.keys())
    comments = parse_comments(analysis_dict_data)
    
    row_idx = 0
    for idx, (competency, avg_score) in enumerate(average_scores.items()):
        readiness_score = df_participant_scores.loc[df_participant_scores['Competency'] == competency, 'SJIT Score'].values[0]
        row_cells = table.add_row().cells
        row_cells[0].text = competency
        row_cells[1].text = str(avg_score)  # Round average score to 2 decimal places
        row_cells[2].text = str(readiness_score)
        row_cells[3].text = comments[idx] if idx < len(comments) else "No comment"  # Replace with your analysis logic

         # Set teal lighter 80% background color for alternating rows
        if row_idx % 2 == 0:
            for cell in row_cells:
                set_cell_background(cell, '#C6F3DE')  # Teal lighter 80%
                set_text_color(cell, RGBColor(0, 0, 0))  # Black text color
                
        row_idx += 1


        # Add borders to the data cells
        for cell in row_cells:
            set_cell_borders(cell, bottom={'val': 'single', 'sz': 4, 'color': 'auto'})

    document.add_page_break()  # Start the new section on a new page
    document.add_heading('Pre And Post Assessment Scores Comparison', level=1)
    document.add_heading('Competency Scores (Average of Application Scores)', level=2)
    # Create a table with the required columns
    table = document.add_table(rows=1, cols=4)
    table.style = 'TableGrid'

    # Set column widths
    table.columns[0].width = Inches(2.5)  # Competency
    table.columns[1].width = Inches(1.5)  # Pre-Assessment Application average
    table.columns[2].width = Inches(1.5)  # Post Assessment Application Average
    table.columns[3].width = Inches(1.5)  # Difference

    # Set column names with centered text and blue background
    headers = ["Competency", "Pre-Assessment Application average", "Post Assessment Application Average", "Difference"]
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        cell.paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, '#4BACC6')  # Light blue color

    # Add data rows
    competencies = list(average_scores.keys())

    for competency, avg_score in average_scores.items():
        readiness_score_pre = df_pre_scores.loc[df_pre_scores['Competency'] == competency, 'PRE_SCORE'].values[0]
        row_cells = table.add_row().cells
        row_cells[0].text = competency
        row_cells[1].text = f"{readiness_score_pre:.2f}"  # Round average score to 2 decimal places
        row_cells[2].text = f"{avg_score:.2f}"
        row_cells[3].text = f"{avg_score - readiness_score_pre:.2f}"

        # Add borders to the data cells
        for cell in row_cells:
            set_cell_borders(cell, bottom={'val': 'single', 'sz': 4, 'color': 'auto'})

    # paragraph_format.line_spacing = 1.75
    document.add_heading('Competency Scores (Average of Readiness Scores)', level=2)
    # Create a table with the required columns
    table = document.add_table(rows=1, cols=4)
    table.style = 'TableGrid'

    # Set column widths
    table.columns[0].width = Inches(2.5)  # Competency Name
    table.columns[1].width = Inches(1.5)  # Pre-Assessment Readiness average	
    table.columns[2].width = Inches(1.5)  # Post Assessment Readiness Average
    table.columns[3].width = Inches(1.5)  # Difference

    # Set column names with centered text and blue background
    headers = ["Competency", "Pre-Assessment Readiness average", "Post Assessment Readiness Average", "Difference"]
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        cell.paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, '00ab41')  # Light green color

    # Add data rows
    competencies = list(average_scores.keys())
    for competency, avg_score in average_scores.items():
        average_scores_read = df_participant_scores.loc[df_participant_scores['Competency'] == competency, 'SJIT Score'].values[0]
        readiness_score = df_pre_readliness_score.loc[df_pre_readliness_score['Competency'] == competency, 'PRE_SCORE_READLINESS'].values[0]
        row_cells = table.add_row().cells
        row_cells[0].text = competency
        row_cells[1].text = f"{average_scores_read:.2f}"  # Round average score to 2 decimal places
        row_cells[2].text = f"{readiness_score:.2f}"
        row_cells[3].text = f"{readiness_score - average_scores_read:.2f}"

        # Add borders to the data cells
        for cell in row_cells:
            set_cell_borders(cell, bottom={'val': 'single', 'sz': 4, 'color': 'auto'})


    # Save the document to a BytesIO stream to return
    stream = BytesIO()
    document.save(stream)
    stream.seek(0)
    return stream
