INSERT INTO Category (id, name)
VALUES
(1, 'Infectious'),
(2, 'Respiratory'),
(3, 'Digestive'),
(4, 'Urinary'),
(5, 'Immune'),
(6, 'Eye'),
(7, 'Endocrine'),
(8, 'Cardiovascular'),
(9, 'Neurological'),
(10, 'Environmental');

INSERT INTO Diseases (id, category_id, name, description, causes, treatment)
VALUES
(1, 1, 'Seasonal Influenza',
 'An acute viral respiratory infection that typically occurs seasonally.',
 'Influenza virus (Type A, B) spread through respiratory droplets from coughing, sneezing, or contact with contaminated surfaces.',
 'Rest, stay hydrated, take paracetamol to reduce fever, and use antiviral medication if diagnosed early.'),

(2, 2, 'Bronchitis',
 'Inflammation of the bronchial tubes lining, causing persistent cough and difficulty breathing.',
 'Viral or bacterial infection, smoking, and long-term exposure to air pollution or dust.',
 'Use expectorants, bronchodilators, antibiotics if bacterial, and avoid smoke and dust exposure.'),

(3, 3, 'Peptic Ulcer Disease',
 'Damage to the stomach lining causing abdominal pain, acid reflux, and indigestion.',
 'Helicobacter pylori infection, overuse of NSAIDs (pain relievers), and chronic stress.',
 'Proton pump inhibitors (PPIs) to reduce acid, antibiotics to eliminate H. pylori, and dietary changes.'),

(4, 4, 'Urinary Tract Infection',
 'A bacterial infection affecting the bladder, urethra, or kidneys, causing painful and frequent urination.',
 'E. coli bacteria entering the urethra, poor personal hygiene, and holding urine for long periods.',
 'Prescribed antibiotics, increased water intake, and proper genital hygiene.'),

(5, 5, 'Systemic Lupus Erythematosus',
 'A chronic autoimmune disease in which the immune system mistakenly attacks the body''s own tissues.',
 'Immune system dysfunction, genetic predisposition, UV light exposure, and certain medications.',
 'Immunosuppressive drugs, corticosteroids, and regular monitoring by a specialist.'),

(6, 6, 'Conjunctivitis',
 'Inflammation of the conjunctiva causing redness, itching, and discharge in the eye.',
 'Viral or bacterial infection, allergies, or irritants such as smoke and chlorine.',
 'Antibiotic or antiviral eye drops, cold compresses, and avoiding touching or rubbing the eyes.'),

(7, 7, 'Type 2 Diabetes',
 'A chronic metabolic disorder in which the body becomes resistant to insulin, leading to high blood sugar.',
 'Obesity, physical inactivity, genetic factors, and a diet high in sugar and refined carbohydrates.',
 'Diet control, regular exercise, and blood sugar-lowering medication or insulin therapy.'),

(8, 8, 'Hypertension',
 'A condition of persistently elevated blood pressure in the arteries, increasing risk of cardiovascular complications.',
 'Genetics, high salt intake, obesity, stress, smoking, and lack of physical activity.',
 'Lifestyle changes, reduced salt intake, and antihypertensive medication as prescribed.'),

(9, 9, 'Migraine',
 'A neurological disorder causing severe, recurring headaches often accompanied by nausea.',
 'Abnormal neurotransmitter activity, genetic factors, stress, and hormonal changes.',
 'Specific migraine medication, resting in a quiet dark room, and avoiding known triggers.'),

(10, 10, 'Heatstroke',
 'A condition where the body overheats due to prolonged exposure to high environmental temperatures.',
 'Prolonged exposure to hot weather, dehydration, and strenuous activity in hot environments.',
 'Move to a cool area, rehydrate with fluids and electrolytes, cool the body down, and seek medical care if severe.');

INSERT INTO Symptoms (id, name, description)
VALUES
(1, 'Fever', 'An abnormal rise in body temperature, often a sign the body is fighting an infection.'),
(2, 'Cough', 'A reflex action to clear the throat or airways of irritants, mucus, or foreign particles.'),
(3, 'Sore Throat', 'Pain, scratchiness, or irritation of the throat that often worsens when swallowing.'),
(4, 'Shortness of Breath', 'Difficulty breathing or a feeling of not getting enough air.'),
(5, 'Abdominal Pain', 'Discomfort or pain felt anywhere between the chest and pelvic region.'),
(6, 'Nausea', 'A feeling of sickness in the stomach with an urge to vomit.'),
(7, 'Painful Urination', 'A burning or stinging sensation while passing urine.'),
(8, 'Frequent Urination', 'The need to urinate more often than usual, including at night.'),
(9, 'Joint Pain', 'Discomfort, soreness, or stiffness in one or more joints of the body.'),
(10, 'Skin Rash', 'A change in the skin''s color, texture, or appearance, often causing redness or itching.'),
(11, 'Red Eyes', 'Redness in the white part of the eye caused by irritation or infection.'),
(12, 'Eye Discharge', 'Fluid, often crusty or watery, that accumulates around the eyes.'),
(13, 'Excessive Thirst', 'An unusually strong urge to drink fluids, often linked to blood sugar imbalance.'),
(14, 'Fatigue', 'A persistent feeling of tiredness or lack of energy, even after rest.'),
(15, 'Headache', 'Pain or discomfort in the head, scalp, or neck region.'),
(16, 'Dizziness', 'A sensation of lightheadedness, unsteadiness, or spinning.'),
(17, 'High Blood Pressure Symptoms', 'Often silent, but may include headaches, blurred vision, or chest discomfort.'),
(18, 'Sensitivity to Light', 'Discomfort or pain in the eyes when exposed to light.'),
(19, 'Excessive Sweating', 'Sweating more than normal, often related to fever or heat exposure.'),
(20, 'Confusion', 'Difficulty thinking clearly, disorientation, or altered mental state.');

INSERT INTO Disease_symptoms (disease_id, symptom_id)
VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 14),
(2, 2),
(2, 4),
(2, 1),
(3, 5),
(3, 6),
(4, 7),
(4, 8),
(4, 1),
(5, 9),
(5, 10),
(5, 14),
(6, 11),
(6, 12),
(6, 18),
(7, 13),
(7, 14),
(7, 8),
(8, 15),
(8, 16),
(8, 17),
(9, 15),
(9, 6),
(9, 18),
(10, 1),
(10, 19),
(10, 16),
(10, 20);

INSERT INTO Prevention (id, disease_id, recommendation)
VALUES
(1, 1, 'Get an annual flu vaccine, wash hands frequently, and avoid close contact with infected individuals.'),
(2, 2, 'Avoid smoking and secondhand smoke, and wear a mask in polluted or dusty environments.'),
(3, 3, 'Avoid excessive use of NSAIDs, limit alcohol intake, and manage stress levels.'),
(4, 4, 'Drink plenty of water, urinate regularly, and maintain proper genital hygiene.'),
(5, 5, 'Avoid excessive sun exposure and follow up regularly with a rheumatologist for early detection.'),
(6, 6, 'Avoid touching or rubbing the eyes, wash hands often, and avoid sharing towels or eye makeup.'),
(7, 7, 'Maintain a healthy weight, exercise regularly, and reduce intake of sugar and refined carbs.'),
(8, 8, 'Reduce salt intake, exercise regularly, and monitor blood pressure periodically.'),
(9, 9, 'Identify and avoid personal migraine triggers, maintain a regular sleep schedule, and manage stress.'),
(10, 10, 'Stay hydrated, avoid strenuous outdoor activity during peak heat hours, and wear light clothing.');

INSERT INTO Emergency_warning (id, disease_id, warning, severity)
VALUES
(1, 1, 'Seek emergency care if experiencing difficulty breathing, chest pain, or persistent high fever.', 'Medium'),
(2, 2, 'Seek immediate medical attention if coughing up blood or experiencing severe shortness of breath.', 'Medium'),
(3, 3, 'Go to the hospital immediately if vomiting blood or passing black, tarry stools.', 'High'),
(4, 4, 'Seek urgent care if fever with chills occurs, which may indicate a kidney infection.', 'Medium'),
(5, 5, 'Seek emergency care for sudden chest pain, severe swelling, or difficulty breathing.', 'High'),
(6, 6, 'See a doctor immediately if experiencing severe eye pain or sudden vision loss.', 'Medium'),
(7, 7, 'Seek emergency care for extreme thirst, confusion, or fruity-smelling breath (signs of ketoacidosis).', 'High'),
(8, 8, 'Seek emergency care immediately for a hypertensive crisis with blood pressure above 180/120 mmHg.', 'High'),
(9, 9, 'Seek immediate care if a headache is sudden, severe, and unlike any previous episode.', 'Medium'),
(10, 10, 'Call emergency services immediately if body temperature exceeds 40°C or the person loses consciousness.', 'High');

INSERT INTO `References` (id, disease_id, organization, url)
VALUES
(1, 1, 'World Health Organization', 'https://www.who.int/health-topics/influenza'),
(2, 2, 'American Lung Association', 'https://www.lung.org/lung-health-diseases/lung-disease-lookup/bronchitis'),
(3, 3, 'Mayo Clinic', 'https://www.mayoclinic.org/diseases-conditions/peptic-ulcer'),
(4, 4, 'National Kidney Foundation', 'https://www.kidney.org/atoz/content/uti'),
(5, 5, 'Lupus Foundation of America', 'https://www.lupus.org'),
(6, 6, 'American Academy of Ophthalmology', 'https://www.aao.org/eye-health/diseases/what-is-conjunctivitis'),
(7, 7, 'American Diabetes Association', 'https://diabetes.org/about-diabetes/type-2'),
(8, 8, 'American Heart Association', 'https://www.heart.org/en/health-topics/high-blood-pressure'),
(9, 9, 'American Migraine Foundation', 'https://americanmigrainefoundation.org'),
(10, 10, 'Centers for Disease Control and Prevention', 'https://www.cdc.gov/disasters/extremeheat/warning.html');

INSERT INTO Usage_statistics (id, feature, created_at)
VALUES
(1, 'Symptom Checker', '2025-01-05 08:30:00'),
(2, 'Disease Search', '2025-01-05 09:15:00'),
(3, 'Chatbot Consultation', '2025-01-06 10:00:00'),
(4, 'Prevention Tips View', '2025-01-06 14:20:00'),
(5, 'Emergency Warning Alert', '2025-01-07 07:45:00'),
(6, 'Symptom Checker', '2025-01-08 11:10:00'),
(7, 'Disease Category Browse', '2025-01-08 16:30:00'),
(8, 'Chatbot Consultation', '2025-01-09 09:05:00'),
(9, 'References View', '2025-01-09 13:40:00'),
(10, 'Symptom Checker', '2025-01-10 18:25:00');

INSERT INTO Chat_history (id, session_id, question, answer, created_at)
VALUES
(1, 'sess-001', 'I have a fever and sore throat, what could it be?',
   'These symptoms are commonly associated with Seasonal Influenza. Please monitor your temperature and rest well.',
   '2025-01-05 08:32:00'),

(2, 'sess-001', 'Should I go to the hospital?',
   'If your fever exceeds 39°C or you experience difficulty breathing, please seek medical attention immediately.',
   '2025-01-05 08:35:00'),

(3, 'sess-002', 'Why do I urinate frequently and feel a burning sensation?',
   'These are common symptoms of a Urinary Tract Infection. It is recommended to increase water intake and consult a doctor.',
   '2025-01-06 10:02:00'),

(4, 'sess-003', 'What causes red and itchy eyes with discharge?',
   'This may indicate Conjunctivitis. Avoid touching your eyes and wash your hands frequently.',
   '2025-01-06 14:22:00'),

(5, 'sess-004', 'I feel very thirsty all the time and tired, is this serious?',
   'Excessive thirst and fatigue can be signs of Type 2 Diabetes. It is advisable to get your blood sugar tested.',
   '2025-01-07 07:47:00'),

(6, 'sess-005', 'What should I do if I have a sudden severe headache?',
   'A sudden, severe headache unlike any before can be a warning sign. Please seek emergency care immediately.',
   '2025-01-08 11:12:00'),

(7, 'sess-006', 'What are ways to prevent the flu?',
   'Getting an annual flu vaccine and washing your hands frequently are effective ways to prevent influenza.',
   '2025-01-08 16:32:00'),

(8, 'sess-007', 'I feel dizzy and my blood pressure seems high.',
   'These may be signs of Hypertension. Please monitor your blood pressure and consult a doctor if it stays high.',
   '2025-01-09 09:07:00'),

(9, 'sess-008', 'How can I tell if my stomach pain is an ulcer?',
   'Persistent abdominal pain along with nausea may indicate a Peptic Ulcer. A medical checkup is recommended.',
   '2025-01-09 13:42:00'),

(10, 'sess-009', 'What should I do during a heatstroke emergency?',
   'Move to a cool area immediately, hydrate with fluids, and seek emergency medical care if symptoms are severe.',
   '2025-01-10 18:27:00');