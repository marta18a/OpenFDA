import http.server
import socketserver
import json
import http.client

#DEFINITIVO



class OpenFDAHTML():


    def get_main_page(self):
        html="""
        <html>
            <head>
                <title>Marta Castillo ortiz</title>
            </head>
            <body>
                <h1 align=CENTER style="font: bold 50px Georgia, serif; color: #6C0324;">OpenFDA Client</h1>
                <div style="background-color: #FFBB5F; border-radius: 25px; padding: 25px; border: 2px solid black; width: 40%">
                    <form method="get"action="listDrugs">
                        <input type= "submit" value ="Drug List: Enviar">
                        </input>
                        <input type= "text" name ="Limit">
                        </input>
                    </form>

                    <form method="get" action = "searchDrug">
                        <input type= "submit" value ="Drug Search: Send to OpenFDA">
                        </input>
                        <input type= "text" name ="drug">
                        </input>
                    </form>
                </div>


                <br>
                <div style="background-color: #FFCE8C; border-radius: 25px; padding: 25px; border: 2px solid black; width: 40%">
                    <form method="get"action="listCompanies">
                        <input type= "submit" value ="Company List: Enviar">
                        </input>
                        <input type= "text" name ="Limit">
                        </input>
                    </form>

                    <form method="get" action = "searchCompany">
                        <input type= "submit" value ="Company Search: Send to OpenFDA">
                        </input>
                        <input type= "text" name ="company">
                        </input>
                    </form>
                </div>


                <br>
                <div style="background-color: #FEDC94; border-radius: 25px; padding: 25px; border: 2px solid black; width: 40%">
                    <form method="get"action="listGender">
                        <input type= "submit" value ="Gender List: Enviar">
                        </input>
                        <input type= "text" name ="Limit">
                        </input>
                    </form>




            </body>
        </html>
        """
        return html

    def get_second_page(self,thing):

            list_html= """
            <html>
                <head>
                    <title>Medicamentos</title>
                </head>
                <body>
                <h1 align=CENTER style="font: bold 50px Georgia, serif; color: #26003E;">Medicamentos</h1>
                <div style="background-color: #DAF7A6 ; border-radius: 25px; margin: auto; padding: 25px; border: 2px solid black; width: 40%;">
                    <ol>
            """

            for i in thing:
                list_html +="<li>"+i+ "</li>"
            list_html += """

                    </ol>
                    </div>
                </body>
            </html>
            """
            return list_html



    def get_not_found_page(self):

        html_not_found="""
         <html>
             <head>
                <h1align=CENTER style="font: bold 50px Georgia, serif; color: #000000;">Error 404, page not found>UPPPPSSSSSSSSS!</h1>
             </head>
             <body>
                <br>
                <div style="background-color: #FECFFF; border-radius: 25px; margin: auto; padding: 25px; border: 18px solid black; width: 40%">
                <h1 align=CENTER style="font: bold 50px Georgia, serif; color: #000000;">Error 404, page not found</h1>
            </body>
        </html>
        """
        return html_not_found

class OpenFDAClient():

    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_EVENT= "/drug/event.json"
    LYRICA= "drug.medicinalproduct"
    OPENFDA_API_DRUG_SEARCH="?limit=10&search=patient.drug.medicinalproduct:"
    OPENFDA_API_COMPANY_SEARCH="?limit=10&search=companynumb:"


    def get_events(self,limite=10): #se conecta con la api fda y obtienen los eventos, se puede pasar el limite...

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL) #El servidor se conierte en cliente http y opnefda nos ofrece apirest ...algo de handler vs openfda
        conn.request("GET", self.OPENFDA_API_EVENT + '?limit='+str(limite))
        r1 = conn.getresponse()
        #200 OK
        data1 = r1.read()
        data= data1.decode("utf8")
        events= data

        return events


    def get_event_search(self,drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)

        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_DRUG_SEARCH+drug)
        r1 = conn.getresponse()
        #200 OK
        data1 = r1.read()
        data= data1.decode("utf8")
        events_drug_search= data

        return events_drug_search


    def get_event_search_company(self,company):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)

        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_COMPANY_SEARCH+company)
        r1 = conn.getresponse()
        #200 OK
        data1 = r1.read()
        data= data1.decode("utf8")
        events_company_search= data

        return events_company_search



class OpenFDAParser():

    def get_drugs_from_events(self,events):
        drugs=[]
        #events_html=""
        for event in events:
            drug=(event['patient']['drug'][0]['medicinalproduct'])
            drugs+=[drug]
        #events_html+=", ".join(drugs)
        return drugs

    def get_companies_from_events(self,events_search):
        companies=[]

        for event in events_search:
            companies+=[event["companynumb"]]

        return companies

    def get_gender_from_events(self, events):
        patients=[]

        for event in events:
            patient=(event['patient']['patientsex'])
            patients+=[patient]

        return patients




# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    #NO_ENCONTRADA= False
    # GET
    def do_GET(self):

        client = OpenFDAClient() #Para crear un objeto. Sin parentesis no crea objetos(clase)
        openfdahtml = OpenFDAHTML()
        parser = OpenFDAParser()



        main_page = False
        is_event = False
        is_drug_search =False
        is_company =False
        is_company_search=False
        is_gender=False
        is_redirect =False
        is_secret=False


        if self.path =="/":
            main_page = True

        elif "/listDrugs" in self.path:
            is_event = True

        elif 'searchDrug' in self.path:
            is_drug_search = True

        elif '/listCompanies' in self.path:
            is_company = True

        elif 'searchCompany'in self.path:
            is_company_search =True

        elif 'listGender' in self.path:
            is_gender =True

        elif '/redirect' in self.path:
            is_redirect=True

        elif '/secret' in self.path:
            is_secret=True




        # Send response status code
        response=200
        # Send headers
        encabezado1='Content-type'
        encabezado2='text/html'
        #self.end_headers()
        # Send message back to client
        #message = "Hello world! " + self.path
        html1= openfdahtml.get_main_page()



        # Write content as utf-8 data

        if main_page:
            #self.wfile.write(bytes(html1, "utf8"))
            html=html1
        elif is_event:
            limite=str(self.path.split('=')[1])
            if limite == '':
                limite =10
            events_str= client.get_events(limite)
            events=json.loads(events_str)
            events=events['results']
            drugs= parser.get_drugs_from_events(events)
            #self.wfile.write(bytes(openfdahtml.get_second_page(drugs), "utf8"))
            html=openfdahtml.get_second_page(drugs)

        elif is_drug_search:
            drug=self.path.split('=')[1]
            events_search=client.get_event_search(drug)
            events_search=json.loads(events_search)
            events1=events_search['results']
            companies=parser.get_companies_from_events(events1)
            html2=openfdahtml.get_second_page(companies)
            #self.wfile.write(bytes(html2,"utf8"))
            html=html2

        elif is_company:
            limite=str(self.path.split('=')[1])
            if limite == '':
                limite =10
            events_str_comp= client.get_events(limite)
            events_comp=json.loads(events_str_comp)
            eventsComp=events_comp['results']
            companies= parser.get_companies_from_events(eventsComp)
            #self.wfile.write(bytes(openfdahtml.get_second_page(companies), "utf8"))
            html=openfdahtml.get_second_page(companies)

        elif is_company_search:
            company=self.path.split('=')[1]
            events_searchComp=client.get_event_search_company(company)
            events_searchComp=json.loads(events_searchComp)
            events2=events_searchComp['results']
            drug_list=parser.get_drugs_from_events(events2)
            html2=openfdahtml.get_second_page(drug_list)
            #self.wfile.write(bytes(html2,"utf8"))
            html=html2

        elif is_gender:
            limite=str(self.path.split('=')[1])
            if limite == '':
                limite =10
            events_str= client.get_events(limite)
            events=json.loads(events_str)
            events=events['results']
            genders= parser.get_gender_from_events(events)
            #self.wfile.write(bytes(openfdahtml.get_second_page(genders), "utf8"))
            html=openfdahtml.get_second_page(genders)

        elif is_redirect:
            response=302
            encabezado1='Location'
            encabezado2='http://localhost:8000/'


        elif is_secret:
            response=401
            encabezado1='WWW-Authenticate'
            encabezado2='Basic realm= "My realm"'

        else:
            #NO_ENCONTRADA=True
            #html3 = """
            #no encuentro nada
            #    """
            response= 404
            #self.wfile.write(bytes(html3, "utf8"))
            html3=openfdahtml.get_not_found_page()
            html=html3
            encabezado1='Content-type'
            encabezado2= 'text/html'

        self.send_response(response)
        # Send headers
        self.send_header(encabezado1,encabezado2)
        self.end_headers()



        if response ==200 or response ==404:
            self.wfile.write(bytes(html, "utf8"))

        return
