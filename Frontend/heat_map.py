from IPython.display import HTML

def heat_map():
    viz_url = "https://public.tableau.com/views/CrimeByAreaMap/CrimebyLocationMap?:language=en-US&publish=yes&:sid=&:display_count=n&:origin=viz_share_link"
    html_code = f'''
    <div class='tableauPlaceholder' id='vizContainer' style='position: relative; width: 100%; height: 800px;'>
        <noscript><a href='#'>
            <img alt='Tableau Visualization' src='{viz_url}.png' style='border: none' />
        </a></noscript>
        <object class='tableauViz' width='100%' height='800' style='display:none;'>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
            <param name='embed_code_version' value='3' /> 
            <param name='site_root' value='' />
            <param name='name' value='CrimeByAreaMap&#47;CrimebyLocationMap' />
            <param name='tabs' value='no' />
            <param name='toolbar' value='yes' />
            <param name='static_image' value='{viz_url}.png' /> 
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='en-US' />
        </object>
    </div>
    <script type='text/javascript'>
        var divElement = document.getElementById('vizContainer');                    
        var vizElement = divElement.getElementsByTagName('object')[0];                    
        vizElement.style.width = '100%';                    
        vizElement.style.height = (divElement.offsetWidth * 0.8) + 'px';                    
        var scriptElement = document.createElement('script');                    
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
        vizElement.parentNode.insertBefore(scriptElement, vizElement);                
    </script>
    '''
    display(HTML(html_code))