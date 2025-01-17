DO $$
DECLARE
    defaultXml varchar := '<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" id="Definitions_1yvrmxl" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="4.0.0">
  <bpmn:collaboration id="Collaboration_0wzn3o2">
    <bpmn:participant id="Participant_1cmbk8y" processRef="Process_13tiqtr" />
  </bpmn:collaboration>
  <bpmn:process id="Process_13tiqtr" isExecutable="true">
    <bpmn:startEvent id="StartEvent_1" />
  </bpmn:process>
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collaboration_0wzn3o2">
      <bpmndi:BPMNShape id="Participant_1cmbk8y_di" bpmnElement="Participant_1cmbk8y" isHorizontal="true">
        <dc:Bounds x="180" y="65" width="600" height="250" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="_BPMNShape_StartEvent_2" bpmnElement="StartEvent_1">
        <dc:Bounds x="272" y="172" width="36" height="36" />
      </bpmndi:BPMNShape>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>
';
    caseXml varchar := '<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:camunda="http://camunda.org/schema/1.0/bpmn" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bioc="http://bpmn.io/schema/bpmn/biocolor/1.0" xmlns:modeler="http://camunda.org/schema/modeler/1.0" id="Definitions_1nk7pui" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="4.7.0" modeler:executionPlatform="Camunda Platform" modeler:executionPlatformVersion="7.15.0">
  <bpmn:collaboration id="Collaboration_0ojchsi">
    <bpmn:participant id="sustav_pool" name="Sustav za prijavu prakse" processRef="Process_0or099w" />
  </bpmn:collaboration>
  <bpmn:process id="Process_0or099w" name="prijava_prakse" isExecutable="true">
    <bpmn:laneSet id="LaneSet_00d2bp4">
      <bpmn:lane id="poslodavac_lane" name="Poslodavac">
        <bpmn:flowNodeRef>razgovor_za_praksu_poslodavac</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>evaluacija_poslodavac</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>student_prihvacen</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>obavijest_odbijanje</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="student_lane" name="Student">
        <bpmn:flowNodeRef>ispunjavanje_prijavnice_student</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>end_event_student</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>predavanje_dnevnika_student</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>start_event_student</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>odabiranje_zadatka_student</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="profesor_lane" name="Profesor">
        <bpmn:flowNodeRef>obavjestavanje_alociranje_student_slack</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_1v1zql0</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>obavjestavanje_studenta_slack_poslodavac</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>obavjestavanje_studenta_email_poslodavac</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_022ukch</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>azuriranje_airtable_student</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>slanje_potvrde_slack_profesor</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_0q2wy8q</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_1b8kjb9</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>slanje_potvrde_email_profesor</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>kreiranje_potvrde_profesor</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>azuriranje_podataka_profesor</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>obavjestavanje_alociranje_student</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>obavjestavanje_poslodavca_student</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>uzimanje_podataka_o_poslodavcu_student</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>potvrda_alociranja_profesor</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>alociranje_profesor</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>studentske_pref</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>
    <bpmn:sequenceFlow id="Flow_1ry7vwa" sourceRef="Gateway_1v1zql0" targetRef="ispunjavanje_prijavnice_student" />
    <bpmn:sequenceFlow id="Flow_0k988op" sourceRef="obavjestavanje_studenta_email_poslodavac" targetRef="Gateway_1v1zql0" />
    <bpmn:sequenceFlow id="Flow_10qrmyc" sourceRef="Gateway_022ukch" targetRef="obavjestavanje_studenta_email_poslodavac" />
    <bpmn:sequenceFlow id="Flow_1cvohty" sourceRef="azuriranje_airtable_student" targetRef="end_event_student" />
    <bpmn:sequenceFlow id="Flow_1jgq625" sourceRef="slanje_potvrde_email_profesor" targetRef="Gateway_0q2wy8q" />
    <bpmn:sequenceFlow id="Flow_0rr5pyh" sourceRef="Gateway_1b8kjb9" targetRef="slanje_potvrde_email_profesor" />
    <bpmn:sequenceFlow id="Flow_1g3f3ei" sourceRef="kreiranje_potvrde_profesor" targetRef="Gateway_1b8kjb9" />
    <bpmn:sequenceFlow id="Flow_1bua3l7" sourceRef="azuriranje_podataka_profesor" targetRef="kreiranje_potvrde_profesor" />
    <bpmn:sequenceFlow id="Flow_1l8y47v" sourceRef="ispunjavanje_prijavnice_student" targetRef="azuriranje_podataka_profesor" />
    <bpmn:sequenceFlow id="Flow_1btfl5a" sourceRef="predavanje_dnevnika_student" targetRef="azuriranje_airtable_student" />
    <bpmn:sequenceFlow id="Flow_03i13r1" sourceRef="Gateway_0q2wy8q" targetRef="predavanje_dnevnika_student" />
    <bpmn:sequenceFlow id="Flow_1cx42m5" sourceRef="razgovor_za_praksu_poslodavac" targetRef="evaluacija_poslodavac" />
    <bpmn:sequenceFlow id="Flow_1rdv20r" name="Da" sourceRef="student_prihvacen" targetRef="Gateway_022ukch">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">kandidat_odobren:true</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="Flow_0eu1nfh" sourceRef="evaluacija_poslodavac" targetRef="student_prihvacen" />
    <bpmn:sequenceFlow id="Flow_0kt3aem" sourceRef="obavjestavanje_alociranje_student_slack" targetRef="razgovor_za_praksu_poslodavac" />
    <bpmn:sequenceFlow id="Flow_1npalzz" name="Ne" sourceRef="student_prihvacen" targetRef="obavijest_odbijanje">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">kandidat_odobren:false</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="Flow_12zi41o" sourceRef="start_event_student" targetRef="odabiranje_zadatka_student" />
    <bpmn:sequenceFlow id="Flow_0lsghyt" sourceRef="alociranje_profesor" targetRef="potvrda_alociranja_profesor" />
    <bpmn:sequenceFlow id="Flow_07vs9rk" sourceRef="potvrda_alociranja_profesor" targetRef="uzimanje_podataka_o_poslodavcu_student" />
    <bpmn:sequenceFlow id="Flow_1vwqbxk" sourceRef="uzimanje_podataka_o_poslodavcu_student" targetRef="obavjestavanje_poslodavca_student" />
    <bpmn:manualTask id="alociranje_profesor" name="Alociranje studenta na zadatak">
      <bpmn:incoming>Flow_0ti6tpk</bpmn:incoming>
      <bpmn:outgoing>Flow_0lsghyt</bpmn:outgoing>
    </bpmn:manualTask>
    <bpmn:userTask id="potvrda_alociranja_profesor" name="Potvrda alociranja">
      <bpmn:documentation>Prvo trebate manualno alocirati studenta, te nakon toga potvrdite</bpmn:documentation>
      <bpmn:extensionElements>
        <camunda:formData>
          <camunda:formField id="potvrda_alociranja" label="Jeste li alocirali studenta" type="yes-no-boolean">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
        </camunda:formData>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_0lsghyt</bpmn:incoming>
      <bpmn:outgoing>Flow_07vs9rk</bpmn:outgoing>
    </bpmn:userTask>
    <bpmn:serviceTask id="uzimanje_podataka_o_poslodavcu_student" name="Dohvat podataka o poslodavcu">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="student_id">${student_id}</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
            <camunda:inputParameter name="url">/allocation</camunda:inputParameter>
            <camunda:inputParameter name="method">GET</camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>airtable</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:outputParameter name="poslodavac_email" />
          <camunda:outputParameter name="kompanija" />
          <camunda:outputParameter name="opis_posla" />
          <camunda:outputParameter name="poslodavac_id" />
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_07vs9rk</bpmn:incoming>
      <bpmn:outgoing>Flow_1vwqbxk</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:userTask id="odabiranje_zadatka_student" name="Odabir preferencija za praksu">
      <bpmn:documentation>Dobro došli na stručnu studentsku praksu. U prvom koraku odabirete svoje preferencije prema listi ponuđenih zadataka i poslodavaca.

Možete izraziti do tri preferencije. Na prvo mjesto stavite svoj prvi odabir.

Dostupne prakse možete vidjeti na https://bit.ly/...</bpmn:documentation>
      <bpmn:extensionElements>
        <camunda:formData>
          <camunda:formField id="ime_student" label="Upišite vaše ime i prezime" type="string">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="zeljeni_poslodavci" label="Odaberite željene poslodavce (do 3, pazite na poredak)" type="autocomplete-string">
            <camunda:properties>
              <camunda:property id="autocomplete_api_location" value="${airtable[url]}/praksa-zadaci" />
            </camunda:properties>
            <camunda:validation>
              <camunda:constraint name="max" config="3" />
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="email_student" label="Upišite vaš email" type="string">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
              <camunda:constraint name="email" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="JMBAG" label="Upišite vaš JMBAG" type="string">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="godina_studija" label="Odaberite na kojoj ste godini studija" type="dropdown">
            <camunda:properties>
              <camunda:property id="dropdown_options" value="3. preddiplomski,1. diplomski,2. diplomski" />
            </camunda:properties>
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="napomena" label="Napišite napomenu ukoliko je potrebno" type="rich-text" />
        </camunda:formData>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_12zi41o</bpmn:incoming>
      <bpmn:incoming>SequenceFlow_0v5m4rx</bpmn:incoming>
      <bpmn:outgoing>Flow_1duw845</bpmn:outgoing>
    </bpmn:userTask>
    <bpmn:startEvent id="start_event_student" name="Započet odabir prakse">
      <bpmn:outgoing>Flow_12zi41o</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:sendTask id="obavjestavanje_poslodavca_student" name="Obavještavanje poslodavca nakon alociranja">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">/email</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="to">${poslodavac_email}</camunda:entry>
                <camunda:entry key="template">poslodavac_after_allocation</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>notification</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="next_task">evaluacija_poslodavac</camunda:inputParameter>
          <camunda:inputParameter name="email_student">${email_student}</camunda:inputParameter>
          <camunda:inputParameter name="ime_student">${ime_student}</camunda:inputParameter>
          <camunda:inputParameter name="godina_studija">${godina_studija}</camunda:inputParameter>
          <camunda:inputParameter name="id_instance" />
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_1vwqbxk</bpmn:incoming>
      <bpmn:outgoing>Flow_0looqv9</bpmn:outgoing>
    </bpmn:sendTask>
    <bpmn:sendTask id="obavjestavanje_alociranje_student" name="Obavjestavanje studenta nakon alociranja email">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">/email</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="to">${email_student}</camunda:entry>
                <camunda:entry key="template">student_after_allocation</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>notification</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="poslodavac_email">${poslodavac_email}</camunda:inputParameter>
          <camunda:inputParameter name="kompanija">${kompanija}</camunda:inputParameter>
          <camunda:inputParameter name="opis_posla">${opis_posla}</camunda:inputParameter>
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_0looqv9</bpmn:incoming>
      <bpmn:outgoing>Flow_177v773</bpmn:outgoing>
    </bpmn:sendTask>
    <bpmn:exclusiveGateway id="student_prihvacen" name="Student prihvacen?">
      <bpmn:incoming>Flow_0eu1nfh</bpmn:incoming>
      <bpmn:outgoing>Flow_1rdv20r</bpmn:outgoing>
      <bpmn:outgoing>Flow_1npalzz</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:userTask id="evaluacija_poslodavac" name="Potvrda evaluacije">
      <bpmn:extensionElements>
        <camunda:formData>
          <camunda:formField id="kandidat_odobren" label="Odobravate li ovog kandidata?" type="yes-no-boolean">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
        </camunda:formData>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_1cx42m5</bpmn:incoming>
      <bpmn:outgoing>Flow_0eu1nfh</bpmn:outgoing>
    </bpmn:userTask>
    <bpmn:userTask id="predavanje_dnevnika_student" name="Predavanje dnevnika prakse">
      <bpmn:documentation>Template za dnevnik dostupan je na http://bit.ly/fipu-praksa-template
Dnevnik je potrebno predati prije prijave ispitnoga roka.</bpmn:documentation>
      <bpmn:extensionElements>
        <camunda:formData>
          <camunda:formField id="potvrda_attachment" label="PDF sken ispunjene potvrde o obavljenoj praksi,  Dostaviti tajnici ili Nikoli Tankoviću i u fizičkom obliku" type="file">
            <camunda:properties>
              <camunda:property id="storage_api_post_location" value="https://fipubot.unipu.hr/file_api/post/file" />
              <camunda:property id="storage_api_get_location" value="https://fipubot.unipu.hr/file_api/public/" />
            </camunda:properties>
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="dnevnik_attachment" label="PDF dnevnika prakse" type="file">
            <camunda:properties>
              <camunda:property id="storage_api_post_location" value="https://fipubot.unipu.hr/file_api/post/file" />
              <camunda:property id="storage_api_get_location" value="https://fipubot.unipu.hr/file_api/public/" />
            </camunda:properties>
          </camunda:formField>
          <camunda:formField id="nastavak_rada" label="Označi ako nastavljaš i dalje raditi u tvrtci ili ćeš ubrzo početi raditi honorarno" type="boolean" />
        </camunda:formData>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_03i13r1</bpmn:incoming>
      <bpmn:outgoing>Flow_1btfl5a</bpmn:outgoing>
    </bpmn:userTask>
    <bpmn:serviceTask id="azuriranje_podataka_profesor" name="Ažuriranje podataka u Airtable">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">/prijavnica</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="student_id">${student_id}</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>airtable</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="kontaktirao_tvrtku">${potvrda_kontaktiranja}</camunda:inputParameter>
          <camunda:inputParameter name="broj_sati">${dogovoreni_broj_sati}</camunda:inputParameter>
          <camunda:inputParameter name="detaljni_opis_zadatka">${detaljni_opis_zadatka}</camunda:inputParameter>
          <camunda:inputParameter name="Poduzeće">${poslodavac_id}</camunda:inputParameter>
          <camunda:inputParameter name="datum_pocetka">${pocetak_prakse}</camunda:inputParameter>
          <camunda:inputParameter name="datum_zavrsetka">${kraj_prakse}</camunda:inputParameter>
          <camunda:inputParameter name="mobitel">${mobitel}</camunda:inputParameter>
          <camunda:inputParameter name="oib">${oib}</camunda:inputParameter>
          <camunda:inputParameter name="Mentor">${mentor}</camunda:inputParameter>
          <camunda:inputParameter name="mail_mentora">${mentor_mail}</camunda:inputParameter>
          <camunda:outputParameter name="prijavnica_id" />
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_1l8y47v</bpmn:incoming>
      <bpmn:outgoing>Flow_1bua3l7</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:serviceTask id="kreiranje_potvrde_profesor" name="Kreiranje potvrde">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">/potvrda</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>pdf</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="email_student">${email_student}</camunda:inputParameter>
          <camunda:inputParameter name="mobitel">${mobitel}</camunda:inputParameter>
          <camunda:inputParameter name="pocetak_prakse">${pocetak_prakse}</camunda:inputParameter>
          <camunda:inputParameter name="kraj_prakse">${kraj_prakse}</camunda:inputParameter>
          <camunda:inputParameter name="oib">${oib}</camunda:inputParameter>
          <camunda:inputParameter name="mentor">${mentor}</camunda:inputParameter>
          <camunda:inputParameter name="dogovoreni_broj_sati">${dogovoreni_broj_sati}</camunda:inputParameter>
          <camunda:inputParameter name="ime_student">${ime_student}</camunda:inputParameter>
          <camunda:inputParameter name="kompanija">${kompanija}</camunda:inputParameter>
          <camunda:inputParameter name="detaljni_opis_zadatka">${detaljni_opis_zadatka}</camunda:inputParameter>
          <camunda:outputParameter name="attachment_url" />
          <camunda:outputParameter name="attachment" />
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_1bua3l7</bpmn:incoming>
      <bpmn:outgoing>Flow_1g3f3ei</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:sendTask id="slanje_potvrde_email_profesor" name="Slanje potvrde o obavljenoj praksi">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="to">${email_student}</camunda:entry>
                <camunda:entry key="template">student_pdf</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
            <camunda:inputParameter name="url">/email</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>notification</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="attachment_name">potvrda.pdf</camunda:inputParameter>
          <camunda:inputParameter name="id_instance" />
          <camunda:inputParameter name="next_task">predavanje_dnevnika_student</camunda:inputParameter>
          <camunda:inputParameter name="attachment_url">${attachment_url}</camunda:inputParameter>
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_0rr5pyh</bpmn:incoming>
      <bpmn:outgoing>Flow_1jgq625</bpmn:outgoing>
    </bpmn:sendTask>
    <bpmn:parallelGateway id="Gateway_1b8kjb9">
      <bpmn:incoming>Flow_1g3f3ei</bpmn:incoming>
      <bpmn:outgoing>Flow_0rr5pyh</bpmn:outgoing>
    </bpmn:parallelGateway>
    <bpmn:parallelGateway id="Gateway_0q2wy8q">
      <bpmn:incoming>Flow_1jgq625</bpmn:incoming>
      <bpmn:outgoing>Flow_03i13r1</bpmn:outgoing>
    </bpmn:parallelGateway>
    <bpmn:sendTask id="slanje_potvrde_slack_profesor" name="Slanje potvrde o obavljenoj praksi slack">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">http://127.0.0.1:8090/notify/student/potvrda/pdf</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="to">${email_student}</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>http-connector</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="id_instance" />
          <camunda:inputParameter name="next_task">predavanje_dnevnika_student</camunda:inputParameter>
          <camunda:inputParameter name="attachment_url">${attachment_url}</camunda:inputParameter>
        </camunda:inputOutput>
      </bpmn:extensionElements>
    </bpmn:sendTask>
    <bpmn:serviceTask id="azuriranje_airtable_student" name="Ažuriranje Airtable">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">/dnevnik</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="prijavnica_id">${prijavnica_id}</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>airtable</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="nastavak_rada">${nastavak_rada}</camunda:inputParameter>
          <camunda:inputParameter name="potvrda_attachment">${potvrda_attachment}</camunda:inputParameter>
          <camunda:inputParameter name="dnevnik_attachment">${dnevnik_attachment}</camunda:inputParameter>
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_1btfl5a</bpmn:incoming>
      <bpmn:outgoing>Flow_1cvohty</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:endEvent id="end_event_student" name="Student prijavio ispit">
      <bpmn:incoming>Flow_1cvohty</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:parallelGateway id="Gateway_022ukch">
      <bpmn:incoming>Flow_1rdv20r</bpmn:incoming>
      <bpmn:outgoing>Flow_10qrmyc</bpmn:outgoing>
    </bpmn:parallelGateway>
    <bpmn:sendTask id="obavjestavanje_studenta_email_poslodavac" name="Obavještavanje studenta email">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">/email</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="to">${email_student}</camunda:entry>
                <camunda:entry key="decision">Approve</camunda:entry>
                <camunda:entry key="template">student_after_approval</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>notification</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="next_task">ispunjavanje_prijavnice_student</camunda:inputParameter>
          <camunda:inputParameter name="id_instance" />
          <camunda:inputParameter name="kompanija">${kompanija}</camunda:inputParameter>
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_10qrmyc</bpmn:incoming>
      <bpmn:outgoing>Flow_0k988op</bpmn:outgoing>
    </bpmn:sendTask>
    <bpmn:sendTask id="obavjestavanje_studenta_slack_poslodavac" name="Obavjestavanje studenta slack">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="to">${email_student}</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
            <camunda:inputParameter name="url">http://127.0.0.1:8090/notify/student/after/approval</camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>http-connector</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="next_task">ispunjavanje_prijavnice_student</camunda:inputParameter>
          <camunda:inputParameter name="id_instance" />
        </camunda:inputOutput>
      </bpmn:extensionElements>
    </bpmn:sendTask>
    <bpmn:parallelGateway id="Gateway_1v1zql0">
      <bpmn:incoming>Flow_0k988op</bpmn:incoming>
      <bpmn:outgoing>Flow_1ry7vwa</bpmn:outgoing>
    </bpmn:parallelGateway>
    <bpmn:userTask id="ispunjavanje_prijavnice_student" name="Ispunjavanje prijavnice">
      <bpmn:documentation>VAŽNO: Prijavnica se popunjava nakon (!) što nastavnik odobri kontakt određenom poduzeću i nakon što student s tim poduzećem dogovori praksu. Popunjenu prijavnicu šaljemo poduzeću na odobrenje i potpis.</bpmn:documentation>
      <bpmn:extensionElements>
        <camunda:formData>
          <camunda:formField id="mentor" label="Ime i prezime mentora iz organizacije" type="string">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="mentor_mail" label="E-mail mentora" type="string">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="pocetak_prakse" label="Odaberite datum pocetka prakse" type="date">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="kraj_prakse" label="Odaberite datum kraja prakse" type="date">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="dogovoreni_broj_sati" label="Dogovoreni broj sati, mora biti između 90 i 150" type="integer">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
              <camunda:constraint name="min" config="90" />
              <camunda:constraint name="max" config="150" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="mobitel" label="Upišite broj mobitela, neće se trajno pohraniti" type="string">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="oib" label="Upišite vaš OIB, za potrebe prijave osiguranja" type="string">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="detaljni_opis_zadatka" label="Detaljno opisati zadatak koji će se izvršavati na praksi" type="rich-text">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
          <camunda:formField id="potvrda_kontaktiranja" label="Potvrđujem da sam kontaktirao tvrtku i dogovorio detalje koji su ovdje uneseni" type="boolean">
            <camunda:validation>
              <camunda:constraint name="required" config="true" />
            </camunda:validation>
          </camunda:formField>
        </camunda:formData>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_1ry7vwa</bpmn:incoming>
      <bpmn:outgoing>Flow_1l8y47v</bpmn:outgoing>
    </bpmn:userTask>
    <bpmn:manualTask id="razgovor_za_praksu_poslodavac" name="Evaluiraj kandidata">
      <bpmn:incoming>Flow_0kt3aem</bpmn:incoming>
      <bpmn:incoming>Flow_177v773</bpmn:incoming>
      <bpmn:outgoing>Flow_1cx42m5</bpmn:outgoing>
    </bpmn:manualTask>
    <bpmn:sendTask id="obavjestavanje_alociranje_student_slack" name="Obavjestavanje studenta nakon alociranja slack">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">http://127.0.0.1:8090//notify/student/after/allocation</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="to">${email_student}</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>http-connector</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="poslodavac_email">${poslodavac_email}</camunda:inputParameter>
          <camunda:inputParameter name="opis_posla">${opis_posla}</camunda:inputParameter>
          <camunda:inputParameter name="kompanija">${kompanija}</camunda:inputParameter>
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:outgoing>Flow_0kt3aem</bpmn:outgoing>
    </bpmn:sendTask>
    <bpmn:sendTask id="obavijest_odbijanje" name="Obavještavanje studenta email">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="url">/email</camunda:inputParameter>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url_parameter">
              <camunda:map>
                <camunda:entry key="to">${email_student}</camunda:entry>
                <camunda:entry key="decision">Reject</camunda:entry>
                <camunda:entry key="template">student_after_approval</camunda:entry>
              </camunda:map>
            </camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>notification</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="next_task">ispunjavanje_prijavnice_student</camunda:inputParameter>
          <camunda:inputParameter name="id_instance" />
          <camunda:inputParameter name="kompanija" />
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_1npalzz</bpmn:incoming>
      <bpmn:outgoing>SequenceFlow_0v5m4rx</bpmn:outgoing>
    </bpmn:sendTask>
    <bpmn:sequenceFlow id="SequenceFlow_0v5m4rx" sourceRef="obavijest_odbijanje" targetRef="odabiranje_zadatka_student" />
    <bpmn:sequenceFlow id="Flow_1duw845" sourceRef="odabiranje_zadatka_student" targetRef="studentske_pref" />
    <bpmn:sequenceFlow id="Flow_0ti6tpk" sourceRef="studentske_pref" targetRef="alociranje_profesor" />
    <bpmn:serviceTask id="studentske_pref" name="Spremanje preferencija u bazu">
      <bpmn:extensionElements>
        <camunda:connector>
          <camunda:inputOutput>
            <camunda:inputParameter name="method">POST</camunda:inputParameter>
            <camunda:inputParameter name="url">/student-preference</camunda:inputParameter>
          </camunda:inputOutput>
          <camunda:connectorId>airtable</camunda:connectorId>
        </camunda:connector>
        <camunda:inputOutput>
          <camunda:inputParameter name="napomena">${napomena}</camunda:inputParameter>
          <camunda:inputParameter name="zeljeni_poslodavci">${zeljeni_poslodavci}</camunda:inputParameter>
          <camunda:inputParameter name="godina_studija">${godina_studija}</camunda:inputParameter>
          <camunda:inputParameter name="ime_student">${ime_student}</camunda:inputParameter>
          <camunda:inputParameter name="JMBAG">${JMBAG}</camunda:inputParameter>
          <camunda:inputParameter name="email_student">${email_student}</camunda:inputParameter>
          <camunda:inputParameter name="id_instance" />
          <camunda:outputParameter name="student_id" />
          <camunda:outputParameter name="alokacija_id" />
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_1duw845</bpmn:incoming>
      <bpmn:outgoing>Flow_0ti6tpk</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:sequenceFlow id="Flow_177v773" sourceRef="obavjestavanje_alociranje_student" targetRef="razgovor_za_praksu_poslodavac" />
    <bpmn:sequenceFlow id="Flow_0looqv9" sourceRef="obavjestavanje_poslodavca_student" targetRef="obavjestavanje_alociranje_student" />
  </bpmn:process>
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collaboration_0ojchsi">
      <bpmndi:BPMNShape id="Participant_1yqxmat_di" bpmnElement="sustav_pool" isHorizontal="true">
        <dc:Bounds x="160" y="80" width="1790" height="570" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Lane_01o4d06_di" bpmnElement="profesor_lane" isHorizontal="true">
        <dc:Bounds x="190" y="430" width="1760" height="220" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Lane_12socvm_di" bpmnElement="student_lane" isHorizontal="true">
        <dc:Bounds x="190" y="250" width="1760" height="180" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Lane_002s8sw_di" bpmnElement="poslodavac_lane" isHorizontal="true">
        <dc:Bounds x="190" y="80" width="1760" height="170" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNEdge id="SequenceFlow_0v5m4rx_di" bpmnElement="SequenceFlow_0v5m4rx">
        <di:waypoint x="361" y="210" />
        <di:waypoint x="361" y="290" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1vwqbxk_di" bpmnElement="Flow_1vwqbxk">
        <di:waypoint x="546" y="490" />
        <di:waypoint x="570" y="490" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_07vs9rk_di" bpmnElement="Flow_07vs9rk">
        <di:waypoint x="496" y="550" />
        <di:waypoint x="496" y="530" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0lsghyt_di" bpmnElement="Flow_0lsghyt">
        <di:waypoint x="411" y="590" />
        <di:waypoint x="446" y="590" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_12zi41o_di" bpmnElement="Flow_12zi41o">
        <di:waypoint x="278" y="330" />
        <di:waypoint x="311" y="330" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1npalzz_di" bpmnElement="Flow_1npalzz" bioc:stroke="#000" bioc:fill="#fff">
        <di:waypoint x="1010" y="145" />
        <di:waypoint x="1010" y="110" />
        <di:waypoint x="361" y="110" />
        <di:waypoint x="361" y="130" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1022" y="113" width="15" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0looqv9_di" bpmnElement="Flow_0looqv9">
        <di:waypoint x="620" y="530" />
        <di:waypoint x="620" y="550" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_177v773_di" bpmnElement="Flow_177v773">
        <di:waypoint x="670" y="590" />
        <di:waypoint x="695" y="590" />
        <di:waypoint x="695" y="170" />
        <di:waypoint x="720" y="170" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0kt3aem_di" bpmnElement="Flow_0kt3aem">
        <di:waypoint x="770" y="550" />
        <di:waypoint x="770" y="210" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0eu1nfh_di" bpmnElement="Flow_0eu1nfh">
        <di:waypoint x="940" y="170" />
        <di:waypoint x="985" y="170" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1rdv20r_di" bpmnElement="Flow_1rdv20r" bioc:stroke="#000" bioc:fill="#fff">
        <di:waypoint x="1010" y="195" />
        <di:waypoint x="1010" y="465" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1022" y="213" width="15" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1cx42m5_di" bpmnElement="Flow_1cx42m5">
        <di:waypoint x="820" y="170" />
        <di:waypoint x="840" y="170" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_03i13r1_di" bpmnElement="Flow_03i13r1">
        <di:waypoint x="1710" y="465" />
        <di:waypoint x="1710" y="380" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1btfl5a_di" bpmnElement="Flow_1btfl5a">
        <di:waypoint x="1760" y="340" />
        <di:waypoint x="1790" y="340" />
        <di:waypoint x="1790" y="570" />
        <di:waypoint x="1820" y="570" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1l8y47v_di" bpmnElement="Flow_1l8y47v">
        <di:waypoint x="1280" y="340" />
        <di:waypoint x="1385" y="340" />
        <di:waypoint x="1385" y="450" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1bua3l7_di" bpmnElement="Flow_1bua3l7">
        <di:waypoint x="1385" y="530" />
        <di:waypoint x="1385" y="550" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1g3f3ei_di" bpmnElement="Flow_1g3f3ei">
        <di:waypoint x="1435" y="590" />
        <di:waypoint x="1475" y="590" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0rr5pyh_di" bpmnElement="Flow_0rr5pyh">
        <di:waypoint x="1500" y="565" />
        <di:waypoint x="1500" y="490" />
        <di:waypoint x="1550" y="490" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1jgq625_di" bpmnElement="Flow_1jgq625">
        <di:waypoint x="1650" y="490" />
        <di:waypoint x="1685" y="490" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1cvohty_di" bpmnElement="Flow_1cvohty">
        <di:waypoint x="1870" y="530" />
        <di:waypoint x="1870" y="348" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_10qrmyc_di" bpmnElement="Flow_10qrmyc">
        <di:waypoint x="1035" y="490" />
        <di:waypoint x="1070" y="490" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0k988op_di" bpmnElement="Flow_0k988op">
        <di:waypoint x="1170" y="490" />
        <di:waypoint x="1205" y="490" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1ry7vwa_di" bpmnElement="Flow_1ry7vwa">
        <di:waypoint x="1230" y="465" />
        <di:waypoint x="1230" y="380" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1duw845_di" bpmnElement="Flow_1duw845">
        <di:waypoint x="361" y="370" />
        <di:waypoint x="361" y="450" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0ti6tpk_di" bpmnElement="Flow_0ti6tpk">
        <di:waypoint x="361" y="530" />
        <di:waypoint x="361" y="550" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNShape id="Activity_0mfxkan_di" bpmnElement="alociranje_profesor">
        <dc:Bounds x="311" y="550" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0fs4rx2_di" bpmnElement="potvrda_alociranja_profesor">
        <dc:Bounds x="446" y="550" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0zb4n41_di" bpmnElement="uzimanje_podataka_o_poslodavcu_student">
        <dc:Bounds x="446" y="450" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_11cml9m_di" bpmnElement="odabiranje_zadatka_student">
        <dc:Bounds x="311" y="290" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Event_1tv7kmn_di" bpmnElement="start_event_student" bioc:stroke="#000" bioc:fill="#fff">
        <dc:Bounds x="242" y="312" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="224" y="355" width="74" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1e62rtc_di" bpmnElement="obavjestavanje_poslodavca_student">
        <dc:Bounds x="570" y="450" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1cxudu2_di" bpmnElement="obavjestavanje_alociranje_student">
        <dc:Bounds x="570" y="550" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_0lnh0cq_di" bpmnElement="student_prihvacen" isMarkerVisible="true" bioc:stroke="#000" bioc:fill="#fff">
        <dc:Bounds x="985" y="145" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1045" y="157" width="54" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1qgovhp_di" bpmnElement="evaluacija_poslodavac">
        <dc:Bounds x="840" y="130" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_176843s_di" bpmnElement="predavanje_dnevnika_student">
        <dc:Bounds x="1660" y="300" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_033wzw3_di" bpmnElement="azuriranje_podataka_profesor">
        <dc:Bounds x="1335" y="450" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0anpsxe_di" bpmnElement="kreiranje_potvrde_profesor">
        <dc:Bounds x="1335" y="550" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1k8zc7b_di" bpmnElement="slanje_potvrde_email_profesor">
        <dc:Bounds x="1550" y="450" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_0bcvwef_di" bpmnElement="Gateway_1b8kjb9">
        <dc:Bounds x="1475" y="565" width="50" height="50" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_1p6bnhj_di" bpmnElement="Gateway_0q2wy8q">
        <dc:Bounds x="1685" y="465" width="50" height="50" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0x083zw_di" bpmnElement="slanje_potvrde_slack_profesor">
        <dc:Bounds x="1550" y="550" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_02sqerr_di" bpmnElement="azuriranje_airtable_student">
        <dc:Bounds x="1820" y="530" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Event_0f6fpdt_di" bpmnElement="end_event_student" bioc:stroke="#000" bioc:fill="#fff">
        <dc:Bounds x="1852" y="312" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1832" y="275" width="76" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_10wwbee_di" bpmnElement="Gateway_022ukch">
        <dc:Bounds x="985" y="465" width="50" height="50" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1tszbn7_di" bpmnElement="obavjestavanje_studenta_email_poslodavac">
        <dc:Bounds x="1070" y="450" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0oeucpk_di" bpmnElement="obavjestavanje_studenta_slack_poslodavac">
        <dc:Bounds x="1070" y="550" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_1i1hvbk_di" bpmnElement="Gateway_1v1zql0">
        <dc:Bounds x="1205" y="465" width="50" height="50" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_10qy04a_di" bpmnElement="ispunjavanje_prijavnice_student">
        <dc:Bounds x="1180" y="300" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1amr003_di" bpmnElement="razgovor_za_praksu_poslodavac">
        <dc:Bounds x="720" y="130" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0gfb0mj_di" bpmnElement="obavjestavanje_alociranje_student_slack">
        <dc:Bounds x="720" y="550" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="SendTask_1e2ea7n_di" bpmnElement="obavijest_odbijanje">
        <dc:Bounds x="311" y="130" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1qsfox4_di" bpmnElement="studentske_pref">
        <dc:Bounds x="311" y="450" width="100" height="80" />
      </bpmndi:BPMNShape>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>';
BEGIN
    INSERT INTO processdefinition(name, filename, xml, is_active, created, last_modified_date, number_of_versions,
                              active_version_id, active_version_number, active_version_name, versions)
    VALUES
        ('Prijava zavrsnog', 'prijavaZavrsnog.bpmn', defaultXml, true, current_timestamp, current_timestamp, 1, 1, 1, 'Prijava zavrsnog v1', ARRAY [1]),
        ('Prijava diplomskog', 'prijavaDiplomskog.bpmn', defaultXml, true, current_timestamp, current_timestamp, 1, 2, 1, 'Prijava diplomskog v1', ARRAY [2]),
        ('Generalne informacije', 'generalInfo.bpmn', defaultXml, true, current_timestamp, current_timestamp, 2, 4, 2, 'Generalne informacije v2', ARRAY [3,4]),
        ('Strucna praksa', 'strucnaPraksa.bpmn', caseXml, true, current_timestamp, current_timestamp, 3, 6, 3, 'Strucna praksa v2', ARRAY [5,6,7]),
        ('Upis u prvu godinu', 'upisPrva.bpmn', defaultXml, true, current_timestamp, current_timestamp, 2, 9, 2, 'Upis u prvu godinu v2', ARRAY [8,9]),
        ('Upis u vise godine', 'upisVisa.bpmn', defaultXml, true, current_timestamp, current_timestamp, 1, 10, 1, 'Upis u vise godine v1', ARRAY [10]),
        ('Ispis', 'ispis.bpmn', defaultXml, true, current_timestamp, current_timestamp, 1, 11, 1, 'Ispis v1', ARRAY [11]),
        ('Gostujuca predavanja', 'predavanja.bpmn', defaultXml, true, current_timestamp, current_timestamp, 1, 12, 1, 'Gostujuca predavanja v1', ARRAY [12]),
        ('Izbor demonstratora', 'demonstratura.bpmn', defaultXml, false, current_timestamp, current_timestamp, 1, null, null, null, ARRAY [13]),
        ('Obavijest', 'obavijest.bpmn', defaultXml, false, current_timestamp, current_timestamp, 1, null, null, null, ARRAY [14]);

    INSERT INTO processversion(name, number, filename, xml, is_active, created, last_modified_date, definition_id)
    VALUES  ('Prijava zavrsnog v1', 1, 'prijavaZavrsnog.bpmn', defaultXml, true, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'prijavaZavrsnog.bpmn' LIMIT 1)),
        ('Prijava diplomskog v1', 1, 'prijavaDiplomskog.bpmn', defaultXml, true, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'prijavaDiplomskog.bpmn' LIMIT 1)),

        ('Generalne informacije v1', 1, 'generalInfo.bpmn', defaultXml, false, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'generalInfo.bpmn' LIMIT 1)),
        ('Generalne informacije v2', 2, 'generalInfo.bpmn', defaultXml, true, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'generalInfo.bpmn' LIMIT 1)),

        ('Strucna praksa v1', 1, 'strucnaPraksa.bpmn', caseXml, false, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'strucnaPraksa.bpmn' LIMIT 1)),
        ('Strucna praksa v2', 2, 'strucnaPraksa.bpmn', caseXml, true, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'strucnaPraksa.bpmn' LIMIT 1)),
        ('Strucna praksa v3', 3, 'strucnaPraksa.bpmn', caseXml, false, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'strucnaPraksa.bpmn' LIMIT 1)),
        ('Upis u prvu godinu v1', 1, 'upisPrva.bpmn', defaultXml, false, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'upisPrva.bpmn' LIMIT 1)),
        ('Upis u prvu godinu v2', 2, 'upisPrva.bpmn', defaultXml, true, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'upisPrva.bpmn' LIMIT 1)),
        ('Upis u vise godine v1', 1, 'upisVisa.bpmn', defaultXml, true, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'upisVisa.bpmn' LIMIT 1)),
        ('Ispis v1', 1, 'ispis.bpmn', defaultXml, true, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'ispis.bpmn' LIMIT 1)),
        ('Gostujuca predavanja v1', 1, 'predavanja.bpmn', defaultXml, true, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'predavanja.bpmn' LIMIT 1)),
        ('Izbor demonstratora v1', 1, 'demonstratura.bpmn', defaultXml, false, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'demonstratura.bpmn' LIMIT 1)),
        ('Obavijest v1', 1, 'obavijest.bpmn', defaultXml, false, current_timestamp, current_timestamp,
         (SELECT id FROM processdefinition WHERE processdefinition.filename = 'obavijest.bpmn' LIMIT 1));


         INSERT INTO public.web_service (id, name, address, created, last_modified_date, is_active) VALUES (2, 'Slackbot', 'http://127.0.0.1:8085', '2022-07-19 08:38:12.643267', '2022-07-19 08:38:12.643267', true);
INSERT INTO public.web_service (id, name, address, created, last_modified_date, is_active) VALUES (3, 'Pdf service', 'http://127.0.0.1:8083', '2022-07-19 08:39:57.959075', '2022-07-19 08:39:57.959075', false);
INSERT INTO public.web_service (id, name, address, created, last_modified_date, is_active) VALUES (4, 'Storage', 'http://127.0.0.1:8084', '2022-07-19 08:39:57.979025', '2022-07-19 08:39:57.979025', true);
INSERT INTO public.web_service (id, name, address, created, last_modified_date, is_active) VALUES (5, 'Notification service', 'http://127.0.0.1:8081', '2022-07-19 08:39:58.021458', '2022-09-03 13:57:37.801575', true);
INSERT INTO public.web_service (id, name, address, created, last_modified_date, is_active) VALUES (1, 'Airtable', 'http://127.0.0.1:8082', '2022-07-19 08:36:50.617825', '2022-07-19 08:36:50.617825', true);

END
$$;
