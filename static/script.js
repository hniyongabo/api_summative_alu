// Tab switching logic
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.getAttribute('data-tab')).classList.add('active');
        document.getElementById('resultsContainer').innerHTML = '';
        document.getElementById('loading').style.display = 'none';
    });
});

// Workout Planner
document.getElementById('workoutForm').addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultsContainer').innerHTML = '';
    const goal = document.getElementById('goal').value;
    const fitness_level = document.getElementById('fitness_level').value;
    const days = document.getElementById('days').value;
    const duration = document.getElementById('duration').value;
    const weeks = document.getElementById('weeks').value;
    const preferences = Array.from(document.querySelectorAll('input[name="preferences"]:checked')).map(cb => cb.value);
    const payload = {
        goal,
        fitness_level,
        preferences,
        health_conditions: ["None"],
        schedule: {
            days_per_week: Number(days),
            session_duration: Number(duration)
        },
        plan_duration_weeks: Number(weeks),
        lang: "en"
    };
    fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        const resultDiv = document.getElementById('resultsContainer');
        resultDiv.innerHTML = '';
        const plan = data.result?.exercises;
        if (!plan || plan.length === 0) {
            resultDiv.textContent = 'No exercises found.';
            return;
        }
        plan.forEach(dayPlan => {
            const daySection = document.createElement('div');
            daySection.classList.add('day');
            const dayTitle = document.createElement('h2');
            dayTitle.textContent = `${dayPlan.day}`;
            daySection.appendChild(dayTitle);
            dayPlan.exercises.forEach(ex => {
                const item = document.createElement('p');
                item.textContent = `- ${ex.name} (${ex.duration}) — Equipment: ${ex.equipment}`;
                daySection.appendChild(item);
            });
            resultDiv.appendChild(daySection);
        });
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultsContainer').textContent = 'Error: ' + error;
    });
});

// Nutrition Planner
document.getElementById('nutritionForm').addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultsContainer').innerHTML = '';
    const goal = document.getElementById('nut_goal').value;
    const dietary_restriction = document.getElementById('dietary_restriction').value;
    const payload = {
        goal,
        diet_type: dietary_restriction,
        lang: "en"
    };
    fetch('/api/nutritionAdvice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultsContainer').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultsContainer').textContent = 'Error: ' + error;
    });
});

// Exercise Details
document.getElementById('exerciseForm').addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultsContainer').innerHTML = '';
    const exercise_name = document.getElementById('exercise_name').value;
    const payload = {
        exercise_name,
        lang: "en"
    };
    fetch('/api/exerciseDetails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultsContainer').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultsContainer').textContent = 'Error: ' + error;
    });
});

// Food Plate Analyzer
document.getElementById('foodplateForm').addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultsContainer').innerHTML = '';
    const imageUrl = document.getElementById('imageUrl').value;
    const payload = {
        imageUrl,
        lang: "en"
    };
    fetch('/api/analyzeFoodPlate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultsContainer').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultsContainer').textContent = 'Error: ' + error;
    });
});