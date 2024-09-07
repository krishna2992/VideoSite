const toggleButton = document.getElementById('searchToggleButton');
        const bottomSearch = document.getElementById('bottomSearch');
        const upperSearch = document.getElementById('upperSearch');

        function toggleBottom()
        {

            if(bottomSearch.style.display === 'none')
            {
                bottomSearch.style.display = 'block';
            }
            else{
                bottomSearch.style.display = 'none';
            }
        }
        function updateUI()
        {
            const windowWidth = window.innerWidth;
            if(windowWidth>600)
            {
                toggleButton.style.display = 'none';
                bottomSearch.style.display = 'none';
                upperSearch.style.display = 'block';
            }
            else{
                toggleButton.style.display = 'block';
                bottomSearch.style.display = 'none';
                upperSearch.style.display = 'none';
            }
        }
        // window.addEventListener('resize', updateUI);
        toggleButton.addEventListener('click', toggleBottom);


