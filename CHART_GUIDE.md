# 📊 Complete Guide: Radar Charts, Donut Charts & Responsiveness

## Table of Contents
1. [What Are These Charts?](#what-are-these-charts)
2. [Radar Chart - Complete Code & Explanation](#radar-chart)
3. [Donut Chart - Complete Code & Explanation](#donut-chart)
4. [Responsiveness - How It Works](#responsiveness)
5. [Complete Workflow](#complete-workflow)

---

## What Are These Charts?

### 🎯 **Radar Chart (Spider Chart)**
- **Looks like:** A spider web with points connected
- **Used for:** Comparing multiple values at once (like comparing 3 health risks)
- **Location in code:** `templates/assessment_detail.html`

### 🍩 **Donut Chart**
- **Looks like:** A donut (circle with hole in center)
- **Used for:** Showing parts of a whole (like showing 3 risk percentages)
- **Location in code:** `templates/dashboard.html`

### 📱 **Responsiveness**
- **What it does:** Makes your website work on phones, tablets, and computers
- **How:** Uses Bootstrap classes and CSS media queries

---

## Radar Chart

### 📍 **Where It's Located**
File: `templates/assessment_detail.html` (lines 97-101 and 384-423)

### 🔧 **Step 1: HTML Canvas Element**
```html
<!-- This creates an empty space where the chart will appear -->
<div class="card">
    <div class="card-body">
        <canvas id="riskChart" height="200"></canvas>
    </div>
</div>
```

**What this does:**
- `<canvas>` = HTML element for drawing graphics
- `id="riskChart"` = unique name so JavaScript can find it
- `height="200"` = sets the height to 200 pixels

### 🔧 **Step 2: JavaScript Code (The Magic!)**
```javascript
// Step 1: Get the canvas element
const ctx = document.getElementById('riskChart').getContext('2d');

// Step 2: Create the chart
new Chart(ctx, {
    type: 'radar',  // ← This tells Chart.js to make a radar chart
    
    // Step 3: Provide the data
    data: {
        labels: ['Cardiovascular', 'Diabetes', 'Hypertension'],
        datasets: [{
            label: 'Risk Score',
            data: [
                {{ assessment.cardiovascular_risk }},  // e.g., 45
                {{ assessment.diabetes_risk }},        // e.g., 30
                {{ assessment.lifestyle_risk }}        // e.g., 60
            ],
            backgroundColor: 'rgba(37, 99, 235, 0.2)',  // Light blue fill
            borderColor: 'rgba(37, 99, 235, 1)',        // Blue border
            borderWidth: 2,                               // Border thickness
            pointBackgroundColor: 'rgba(37, 99, 235, 1)' // Blue dots
        }]
    },
    
    // Step 4: Configure options
    options: {
        responsive: true,  // ← Makes it resize automatically
        scales: {
            r: {  // 'r' stands for radial (the circles in radar chart)
                beginAtZero: true,  // Start from 0
                max: 100,           // Go up to 100
                ticks: {
                    stepSize: 25    // Show lines at 0, 25, 50, 75, 100
                }
            }
        },
        plugins: {
            legend: {
                display: false  // Hide the legend (we don't need it)
            }
        }
    }
});
```

### 📖 **Line-by-Line Explanation**

| Line | What It Does |
|------|-------------|
| `const ctx = ...` | Gets the canvas element and prepares it for drawing |
| `new Chart(...)` | Creates a new chart using Chart.js library |
| `type: 'radar'` | Specifies we want a radar chart |
| `labels: [...]` | Names for each point (3 health categories) |
| `data: [...]` | The actual numbers to display |
| `backgroundColor` | Color inside the shape (light blue, 20% opacity) |
| `borderColor` | Color of the border line (solid blue) |
| `responsive: true` | Chart automatically resizes on different screens |
| `beginAtZero: true` | Chart always starts at 0 |
| `max: 100` | Chart goes up to 100 (percentage) |

### 🎨 **Visual Result**
```
        Hypertension (60%)
              |
              |
    Diabetes (30%) ---- Cardiovascular (45%)
              |
              |
```

---

## Donut Chart

### 📍 **Where It's Located**
File: `templates/dashboard.html` (lines 159 and 285-317)

### 🔧 **Step 1: HTML Canvas Element**
```html
<div class="col-md-6">
    <canvas id="riskChart" height="200"></canvas>
</div>
```

**What this does:**
- Same as radar chart - creates space for the chart
- `col-md-6` = Bootstrap class (takes half width on medium+ screens)

### 🔧 **Step 2: JavaScript Code**
```javascript
// Step 1: Get the canvas element
const ctx = document.getElementById('riskChart').getContext('2d');

// Step 2: Create the donut chart
new Chart(ctx, {
    type: 'doughnut',  // ← This tells Chart.js to make a donut chart
    
    // Step 3: Provide the data
    data: {
        labels: ['Cardiovascular', 'Diabetes', 'Hypertension'],
        datasets: [{
            data: [
                {{ latest_assessment.cardiovascular_risk }},  // e.g., 45
                {{ latest_assessment.diabetes_risk }},        // e.g., 30
                {{ latest_assessment.lifestyle_risk }}        // e.g., 25
            ],
            backgroundColor: [
                'rgba(239, 68, 68, 0.8)',   // Red for Cardiovascular
                'rgba(245, 158, 11, 0.8)',  // Orange for Diabetes
                'rgba(37, 99, 235, 0.8)'    // Blue for Hypertension
            ],
            borderWidth: 0  // No border around slices
        }]
    },
    
    // Step 4: Configure options
    options: {
        responsive: true,              // Auto-resize
        maintainAspectRatio: false,    // Don't keep fixed ratio
        plugins: {
            legend: {
                position: 'bottom'     // Show legend below chart
            }
        },
        cutout: '60%'                  // ← This creates the hole! (60% = big hole)
    }
});
```

### 📖 **Key Differences from Radar Chart**

| Feature | Radar Chart | Donut Chart |
|---------|-------------|-------------|
| **Type** | `'radar'` | `'doughnut'` |
| **Shows** | Comparison of values | Parts of a whole |
| **Colors** | One color | Multiple colors (one per slice) |
| **Special Option** | `scales: { r: {...} }` | `cutout: '60%'` |
| **Legend** | Hidden | Shown at bottom |

### 🎨 **Visual Result**
```
    ┌─────────────────┐
    │   [Red Slice]   │  ← Cardiovascular (45%)
    │  [Orange Slice] │  ← Diabetes (30%)
    │   [Blue Slice]  │  ← Hypertension (25%)
    │                 │
    │    (Hole)       │  ← Empty center (60% cutout)
    └─────────────────┘
```

### 🔑 **Important Settings Explained**

1. **`cutout: '60%'`**
   - Creates the hole in the center
   - `60%` means 60% of the radius is empty
   - Change to `'50%'` for smaller hole, `'70%'` for bigger hole

2. **`maintainAspectRatio: false`**
   - Allows chart to stretch/shrink freely
   - Needed for responsive design

3. **Multiple Colors**
   - Each slice gets its own color from the array
   - `rgba(239, 68, 68, 0.8)` = Red with 80% opacity

---

## Responsiveness

### 📍 **Where It's Located**
- Bootstrap classes: Throughout all HTML files
- CSS: `templates/base.html` (lines 1-448)
- Viewport meta tag: `templates/base.html` (line 5)

### 🔧 **Step 1: Viewport Meta Tag**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**What this does:**
- Tells browser: "This website is mobile-friendly"
- `width=device-width` = Use device's screen width
- `initial-scale=1.0` = Start at 100% zoom (no zoom)

### 🔧 **Step 2: Bootstrap Grid System**

Bootstrap uses a 12-column grid system. Here's how it works:

```html
<!-- Example from dashboard.html -->
<div class="row g-4 mb-5">
    <!-- Takes full width on mobile, half on tablet, quarter on desktop -->
    <div class="col-md-6 col-lg-3">
        <div class="stat-card">...</div>
    </div>
</div>
```

**Breakdown:**
- `row` = Container for columns
- `g-4` = Gap of 4 units between columns
- `col-md-6` = On medium screens (tablets), take 6/12 = 50% width
- `col-lg-3` = On large screens (desktops), take 3/12 = 25% width
- **On mobile:** Takes full width (100%) by default

### 📱 **Bootstrap Breakpoints**

| Class Prefix | Screen Size | Example Device |
|--------------|-------------|----------------|
| (none) | < 576px | Small phones |
| `sm` | ≥ 576px | Large phones |
| `md` | ≥ 768px | Tablets |
| `lg` | ≥ 992px | Small laptops |
| `xl` | ≥ 1200px | Desktops |
| `xxl` | ≥ 1400px | Large desktops |

### 🔧 **Step 3: Responsive Chart Settings**

```javascript
options: {
    responsive: true,  // ← This is the key!
    maintainAspectRatio: false  // For donut charts
}
```

**What `responsive: true` does:**
- Chart automatically detects container size
- Resizes when window is resized
- Works on all screen sizes

### 🔧 **Step 4: CSS Media Queries (Advanced)**

In `base.html`, you can add custom responsive CSS:

```css
/* Example: Hide something on small screens */
@media (max-width: 768px) {
    .hide-on-mobile {
        display: none;
    }
}

/* Example: Smaller font on mobile */
@media (max-width: 576px) {
    .display-5 {
        font-size: 1.5rem !important;
    }
}
```

### 📖 **Common Responsive Patterns**

| Pattern | Code | Result |
|---------|------|--------|
| **Stack on mobile, side-by-side on desktop** | `col-md-6` | Mobile: 100%, Desktop: 50% |
| **Always full width** | `col-12` | 100% on all screens |
| **3 columns on desktop, 1 on mobile** | `col-md-4` | Mobile: 100%, Desktop: 33% |
| **Hide on mobile** | `d-none d-md-block` | Hidden on mobile, shown on tablet+ |

---

## Complete Workflow

### 🎬 **How Everything Works Together**

#### **1. User Opens Assessment Detail Page**

```
User clicks "View Details" 
    ↓
Django loads assessment_detail.html
    ↓
HTML renders with canvas element: <canvas id="riskChart">
    ↓
Page finishes loading
    ↓
JavaScript runs (in {% block extra_js %})
    ↓
Chart.js library creates radar chart
    ↓
Chart displays on screen
```

#### **2. User Opens Dashboard**

```
User clicks "Dashboard"
    ↓
Django loads dashboard.html
    ↓
HTML renders with canvas: <canvas id="riskChart">
    ↓
Page finishes loading
    ↓
JavaScript runs (in {% block extra_js %})
    ↓
Chart.js library creates donut chart
    ↓
Chart displays on screen
```

#### **3. User Resizes Browser Window**

```
User drags browser window smaller
    ↓
Browser detects size change
    ↓
Bootstrap classes recalculate widths
    ↓
Chart.js detects container size change (responsive: true)
    ↓
Chart automatically redraws at new size
    ↓
Everything still looks good!
```

### 🔄 **Data Flow**

```
Django Backend (Python)
    ↓
    Calculates risk scores
    ↓
    Passes to template: {{ assessment.cardiovascular_risk }}
    ↓
HTML Template
    ↓
    Renders numbers in JavaScript: data: [45, 30, 60]
    ↓
Chart.js Library
    ↓
    Reads data and draws chart
    ↓
Browser Canvas Element
    ↓
    Displays beautiful chart!
```

### 📋 **Step-by-Step: Creating a Chart**

1. **Include Chart.js Library** (in `base.html`)
   ```html
   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
   ```

2. **Add Canvas Element** (in your template)
   ```html
   <canvas id="myChart"></canvas>
   ```

3. **Write JavaScript** (in `{% block extra_js %}`)
   ```javascript
   const ctx = document.getElementById('myChart').getContext('2d');
   new Chart(ctx, {
       type: 'radar',  // or 'doughnut'
       data: { ... },
       options: { responsive: true }
   });
   ```

4. **Test Responsiveness**
   - Open browser DevTools (F12)
   - Click device toggle icon
   - Test on different screen sizes

---

## 🎯 Quick Reference

### Radar Chart Template
```javascript
const ctx = document.getElementById('riskChart').getContext('2d');
new Chart(ctx, {
    type: 'radar',
    data: {
        labels: ['Label1', 'Label2', 'Label3'],
        datasets: [{
            data: [value1, value2, value3],
            backgroundColor: 'rgba(37, 99, 235, 0.2)',
            borderColor: 'rgba(37, 99, 235, 1)',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        scales: {
            r: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});
```

### Donut Chart Template
```javascript
const ctx = document.getElementById('riskChart').getContext('2d');
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Label1', 'Label2', 'Label3'],
        datasets: [{
            data: [value1, value2, value3],
            backgroundColor: [
                'rgba(239, 68, 68, 0.8)',
                'rgba(245, 158, 11, 0.8)',
                'rgba(37, 99, 235, 0.8)'
            ]
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '60%',
        plugins: {
            legend: { position: 'bottom' }
        }
    }
});
```

### Responsive HTML Template
```html
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">
        <!-- Content here -->
    </div>
</div>
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Chart Not Showing
**Solution:** Make sure Chart.js is loaded before your script
```html
<!-- ✅ Correct order -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Your chart code here
</script>
```

### Issue 2: Chart Too Small on Mobile
**Solution:** Add height to canvas or use `maintainAspectRatio: false`
```html
<canvas id="riskChart" height="300"></canvas>
```

### Issue 3: Chart Not Resizing
**Solution:** Make sure `responsive: true` is set
```javascript
options: {
    responsive: true  // ← Don't forget this!
}
```

---

## 📚 Additional Resources

- **Chart.js Documentation:** https://www.chartjs.org/docs/
- **Bootstrap Grid:** https://getbootstrap.com/docs/5.3/layout/grid/
- **Responsive Design Guide:** https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design

---

**Happy Coding! 🚀**
