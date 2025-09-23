// Main JavaScript for School Data Explorer
class SchoolDataExplorer {
    constructor() {
        this.allData = JSON.parse(document.getElementById('data-script').textContent);
        this.initializeElements();
        this.setupEventListeners();
        this.updateSchools();
        this.updateAllCostsAndDetails();
    }

    initializeElements() {
        // Form elements
        this.districtSelect = document.getElementById('district');
        this.rfpTypeSelect = document.getElementById('rfp-type');
        this.schoolCheckboxContainer = document.getElementById('school-checkbox-container');
        this.selectAllSchoolsCheckbox = document.getElementById('select-all-schools');
        
        // Program configuration inputs (all editable)
        this.weeksInput = document.getElementById('weeks-input');
        this.daysInput = document.getElementById('days-input');
        this.totalStudentsInput = document.getElementById('total-students-input');
        this.hoursPerDayInput = document.getElementById('hours-per-day-input');
        this.costPerStudentInputEditable = document.getElementById('cost-per-student-input-editable');
        this.costPerHourInput = document.getElementById('cost-per-hour-input');
        this.maxSchoolsInput = document.getElementById('max-schools-input');
        this.programCapacityInput = document.getElementById('program-capacity-input');
        
        // Cost summary elements
        this.dailyCostInput = document.getElementById('daily-cost-input');
        this.weeklyCostInput = document.getElementById('weekly-cost-input');
        this.costProposalInput = document.getElementById('cost-proposal-input');
        
        // Form and UI elements
        this.proposalForm = document.getElementById('proposal-form');
        this.generateBtn = document.getElementById('generate-btn');
        this.loader = document.getElementById('loader');
        
        // School funding table elements
        this.schoolFundingCard = document.getElementById('school-funding-card');
        this.schoolFundingBody = document.getElementById('school-funding-body');
        this.totalActualEnrollmentFooter = document.getElementById('total-actual-enrollment-footer');
        
        // Hidden inputs for backend
        this.hiddenInputs = {
            totalStudents: document.getElementById('total-students-for-ai-hidden'),
            costPerStudent: document.getElementById('cost-per-student-for-ai-hidden'),
            hoursPerDay: document.getElementById('hours-per-day-for-ai-hidden'),
            dailyCost: document.getElementById('daily-cost-for-ai-hidden'),
            weeklyCost: document.getElementById('weekly-cost-for-ai-hidden')
        };

        // Constants for validation
        this.CONSTANTS = {
            PER_STUDENT_FUNDING: 2500,
            MAX_STUDENTS_DEFAULT: 200,
            MAX_HOURS_DEFAULT: 12,
            MAX_COST_PER_STUDENT_DEFAULT: 100.00,
            MAX_WEEKS_DEFAULT: 52,
            MAX_SCHOOLS_DEFAULT: 10
        };
    }

    setupEventListeners() {
        // District and RFP type changes
        this.districtSelect.addEventListener('change', () => this.updateSchools());
        this.rfpTypeSelect.addEventListener('change', () => this.updateConstraints());

        // School selection
        this.selectAllSchoolsCheckbox.addEventListener('change', () => this.handleSelectAllSchools());

        // Program configuration changes (all editable fields)
        this.totalStudentsInput.addEventListener('input', () => this.handleStudentsChange());
        this.weeksInput.addEventListener('input', () => this.handleWeeksChange());
        this.daysInput.addEventListener('change', () => this.updateAllCostsAndDetails());
        this.hoursPerDayInput.addEventListener('input', () => this.handleHoursChange());
        this.costPerStudentInputEditable.addEventListener('input', () => this.handleCostPerStudentChange());
        this.maxSchoolsInput.addEventListener('input', () => this.handleMaxSchoolsChange());

        // Form submission
        this.proposalForm.addEventListener('submit', (e) => this.handleFormSubmission(e));

        // Real-time validation
        this.setupRealTimeValidation();
    }

    setupRealTimeValidation() {
        // Add real-time validation for all numeric inputs
        const numericInputs = [
            this.totalStudentsInput,
            this.weeksInput,
            this.hoursPerDayInput,
            this.costPerStudentInputEditable,
            this.maxSchoolsInput
        ];

        numericInputs.forEach(input => {
            if (input) {
                input.addEventListener('blur', () => this.validateInput(input));
                input.addEventListener('input', () => this.clearValidationMessage(input));
            }
        });
    }

    validateInput(input) {
        const value = parseFloat(input.value);
        const min = parseFloat(input.min) || 0;
        const max = parseFloat(input.max) || Infinity;
        
        if (isNaN(value) || value < min || value > max) {
            this.showValidationMessage(input, `Please enter a value between ${min} and ${max}`);
            return false;
        }
        
        this.clearValidationMessage(input);
        return true;
    }

    updateConstraints() {
        const rfpType = this.rfpTypeSelect.value;
        
        // Update constraints display based on current values
        this.updateConstraintDisplay();
        
        // Update school selection constraints
        this.enforceMaxSchools();
    }

    updateConstraintDisplay() {
        const maxStudents = parseInt(this.totalStudentsInput.max) || this.CONSTANTS.MAX_STUDENTS_DEFAULT;
        const maxHours = parseInt(this.hoursPerDayInput.max) || this.CONSTANTS.MAX_HOURS_DEFAULT;
        const maxCostPerStudent = parseFloat(this.costPerStudentInputEditable.max) || this.CONSTANTS.MAX_COST_PER_STUDENT_DEFAULT;
        const maxWeeks = parseInt(this.weeksInput.max) || this.CONSTANTS.MAX_WEEKS_DEFAULT;
        const maxSchools = parseInt(this.maxSchoolsInput.max) || this.CONSTANTS.MAX_SCHOOLS_DEFAULT;
        
        const currentCostPerStudent = parseFloat(this.costPerStudentInputEditable.value) || 20;
        const currentHours = parseFloat(this.hoursPerDayInput.value) || 3;
        const costPerHour = currentCostPerStudent / currentHours;

        const constraintsInfo = document.querySelector('.constraints-info ul');
        if (constraintsInfo) {
            constraintsInfo.innerHTML = `
                <li>Maximum ${maxStudents} students per day (current: ${this.totalStudentsInput.value})</li>
                <li>1-${maxHours} hours per day per session (current: ${this.hoursPerDayInput.value})</li>
                <li>$1-${maxCostPerStudent} per student per day (current: ${currentCostPerStudent}, ${costPerHour.toFixed(2)} per hour)</li>
                <li>1 or 2 days per week available (current: ${this.daysInput.value})</li>
                <li>Maximum ${maxSchools} schools can be served (current: ${this.maxSchoolsInput.value})</li>
                <li>Available for 1-${maxWeeks} weeks (current: ${this.weeksInput.value})</li>
            `;
        }
    }

    formatCurrency(value) {
        if (isNaN(value) || value === null) {
            return "$0.00";
        }
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
    }

    updateSchools() {
        const selectedDistrict = this.districtSelect.value;
        const schoolsInDistrict = this.allData.filter(row => row['District Name'] === selectedDistrict);

        this.schoolCheckboxContainer.innerHTML = "";
        this.selectAllSchoolsCheckbox.checked = false;

        if (schoolsInDistrict.length === 0) {
            this.schoolFundingCard.style.display = 'none';
            return;
        }

        schoolsInDistrict.forEach((school, index) => {
            const schoolName = school['School Name'];
            const checkboxId = `school-${index}`;

            const itemDiv = document.createElement('div');
            itemDiv.className = 'checkbox-item';

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.name = 'schoolname';
            checkbox.value = schoolName;
            checkbox.id = checkboxId;
            checkbox.dataset.schoolData = JSON.stringify(school);
            checkbox.addEventListener('change', () => {
                this.enforceMaxSchools();
                this.updateAllCostsAndDetails();
            });

            const label = document.createElement('label');
            label.htmlFor = checkboxId;
            label.textContent = schoolName;

            itemDiv.appendChild(checkbox);
            itemDiv.appendChild(label);
            this.schoolCheckboxContainer.appendChild(itemDiv);
        });

        this.updateAllCostsAndDetails();
    }

    enforceMaxSchools() {
        const maxSchools = parseInt(this.maxSchoolsInput.value) || 5;
        const checkedBoxes = document.querySelectorAll('input[name="schoolname"]:checked');
        const allBoxes = document.querySelectorAll('input[name="schoolname"]');
        
        if (checkedBoxes.length >= maxSchools) {
            allBoxes.forEach(box => {
                if (!box.checked) {
                    box.disabled = true;
                }
            });
            if (checkedBoxes.length < allBoxes.length) {
                this.selectAllSchoolsCheckbox.disabled = true;
            }
        } else {
            allBoxes.forEach(box => {
                box.disabled = false;
            });
            this.selectAllSchoolsCheckbox.disabled = false;
        }
    }

    handleSelectAllSchools() {
        const isChecked = this.selectAllSchoolsCheckbox.checked;
        const schoolCheckboxes = this.schoolCheckboxContainer.querySelectorAll('input[name="schoolname"]:not(:disabled)');
        const maxSchools = parseInt(this.maxSchoolsInput.value) || 5;
        
        if (isChecked) {
            let checkedCount = 0;
            schoolCheckboxes.forEach(checkbox => {
                if (checkedCount < maxSchools) {
                    checkbox.checked = true;
                    checkedCount++;
                }
            });
        } else {
            schoolCheckboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
        }
        
        this.enforceMaxSchools();
        this.updateAllCostsAndDetails();
    }

    handleStudentsChange() {
        const value = parseInt(this.totalStudentsInput.value, 10);
        const max = parseInt(this.totalStudentsInput.max) || this.CONSTANTS.MAX_STUDENTS_DEFAULT;
        
        if (value > max) {
            this.totalStudentsInput.value = max;
            this.showValidationMessage(this.totalStudentsInput, `Maximum ${max} students allowed`);
        } else {
            this.clearValidationMessage(this.totalStudentsInput);
        }
        this.updateConstraintDisplay();
        this.updateAllCostsAndDetails();
    }

    handleWeeksChange() {
        const value = parseInt(this.weeksInput.value, 10);
        const max = parseInt(this.weeksInput.max) || this.CONSTANTS.MAX_WEEKS_DEFAULT;
        
        if (value > max) {
            this.weeksInput.value = max;
            this.showValidationMessage(this.weeksInput, `Maximum ${max} weeks allowed`);
        } else {
            this.clearValidationMessage(this.weeksInput);
        }
        this.updateConstraintDisplay();
        this.updateAllCostsAndDetails();
    }

    handleHoursChange() {
        const value = parseFloat(this.hoursPerDayInput.value);
        const max = parseFloat(this.hoursPerDayInput.max) || this.CONSTANTS.MAX_HOURS_DEFAULT;
        
        if (value > max) {
            this.hoursPerDayInput.value = max;
            this.showValidationMessage(this.hoursPerDayInput, `Maximum ${max} hours allowed`);
        } else {
            this.clearValidationMessage(this.hoursPerDayInput);
        }
        this.updateCostPerHour();
        this.updateConstraintDisplay();
        this.updateAllCostsAndDetails();
    }

    handleCostPerStudentChange() {
        const value = parseFloat(this.costPerStudentInputEditable.value);
        const max = parseFloat(this.costPerStudentInputEditable.max) || this.CONSTANTS.MAX_COST_PER_STUDENT_DEFAULT;
        
        if (value > max) {
            this.costPerStudentInputEditable.value = max;
            this.showValidationMessage(this.costPerStudentInputEditable, `Maximum ${max} per student allowed`);
        } else {
            this.clearValidationMessage(this.costPerStudentInputEditable);
        }
        this.updateCostPerHour();
        this.updateConstraintDisplay();
        this.updateAllCostsAndDetails();
    }

    handleMaxSchoolsChange() {
        const value = parseInt(this.maxSchoolsInput.value);
        const max = parseInt(this.maxSchoolsInput.max) || this.CONSTANTS.MAX_SCHOOLS_DEFAULT;
        
        if (value > max) {
            this.maxSchoolsInput.value = max;
            this.showValidationMessage(this.maxSchoolsInput, `Maximum ${max} schools allowed`);
        } else {
            this.clearValidationMessage(this.maxSchoolsInput);
        }
        
        // Update school selection constraints
        this.enforceMaxSchools();
        this.updateConstraintDisplay();
        this.updateAllCostsAndDetails();
    }

    updateCostPerHour() {
        const costPerStudent = parseFloat(this.costPerStudentInputEditable.value) || 0;
        const hoursPerDay = parseFloat(this.hoursPerDayInput.value) || 1;
        const costPerHour = costPerStudent / hoursPerDay;
        this.costPerHourInput.value = this.formatCurrency(costPerHour);
    }

    updateProgramCapacity() {
        const studentsPerDay = parseInt(this.totalStudentsInput.value) || 0;
        const maxSchools = parseInt(this.maxSchoolsInput.value) || 1;
        const totalCapacity = studentsPerDay * maxSchools;
        this.programCapacityInput.value = `${totalCapacity.toLocaleString()} students total`;
    }

    showValidationMessage(element, message) {
        element.classList.add('input-error');
        let errorDiv = element.parentElement.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            element.parentElement.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }

    clearValidationMessage(element) {
        element.classList.remove('input-error');
        const errorDiv = element.parentElement.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    calculateFunding(schoolData) {
        const enrollment = parseInt(schoolData['Total Enrollment'], 10) || 0;
        const frmpPercent = parseFloat(schoolData['FRPM Percent (%)']) / 100 || 0;
        return enrollment * frmpPercent * this.CONSTANTS.PER_STUDENT_FUNDING;
    }

    updateAllCostsAndDetails() {
        const numSchoolsSelected = document.querySelectorAll('input[name="schoolname"]:checked').length;
        const studentsPerDay = parseInt(this.totalStudentsInput.value, 10) || 0;
        const daysPerWeek = parseInt(this.daysInput.value, 10) || 1;
        const weeks = parseInt(this.weeksInput.value, 10) || 1;
        const hoursPerDay = parseFloat(this.hoursPerDayInput.value) || 3;
        const costPerStudentPerDay = parseFloat(this.costPerStudentInputEditable.value) || 20;

        let totalActualEnrollment = 0;
        
        this.schoolFundingBody.innerHTML = '';

        if (numSchoolsSelected > 0) {
            this.schoolFundingCard.style.display = 'block';
            document.querySelectorAll('input[name="schoolname"]:checked').forEach(checkbox => {
                const schoolData = JSON.parse(checkbox.dataset.schoolData);
                const enrollment = parseInt(schoolData['Total Enrollment'], 10) || 0;
                const schoolFunding = this.calculateFunding(schoolData);

                totalActualEnrollment += enrollment;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${schoolData['School Name']}</td>
                    <td>${enrollment.toLocaleString()}</td>
                    <td>${(parseFloat(schoolData['FRPM Percent (%)']) || 0).toFixed(2)}%</td>
                    <td>${this.formatCurrency(schoolFunding)}</td>
                `;
                this.schoolFundingBody.appendChild(row);
            });
        } else {
            this.schoolFundingCard.style.display = 'none';
        }

        this.totalActualEnrollmentFooter.textContent = totalActualEnrollment.toLocaleString();

        // Calculate costs
        const dailyCost = studentsPerDay * costPerStudentPerDay;
        const weeklyCost = dailyCost * daysPerWeek;
        const totalProgramCost = weeklyCost * weeks;

        // Update cost displays
        this.dailyCostInput.value = this.formatCurrency(dailyCost);
        this.weeklyCostInput.value = this.formatCurrency(weeklyCost);
        this.costProposalInput.value = this.formatCurrency(totalProgramCost);

        // Update program capacity
        this.updateProgramCapacity();

        // Update hidden inputs for backend submission
        this.hiddenInputs.totalStudents.value = studentsPerDay;
        this.hiddenInputs.costPerStudent.value = costPerStudentPerDay.toFixed(2);
        this.hiddenInputs.hoursPerDay.value = hoursPerDay;
        this.hiddenInputs.dailyCost.value = dailyCost.toFixed(2);
        this.hiddenInputs.weeklyCost.value = weeklyCost.toFixed(2);
    }

    handleFormSubmission(event) {
        this.updateAllCostsAndDetails();

        // Validate all fields before submission
        const isValid = this.validateAllFields();
        
        if (!isValid) {
            event.preventDefault();
            return;
        }

        this.generateBtn.style.display = 'none';
        this.loader.style.display = 'block';
    }

    validateAllFields() {
        const selectedCheckboxes = document.querySelectorAll('input[name="schoolname"]:checked');
        const maxSchools = parseInt(this.maxSchoolsInput.value) || 5;
        
        if (selectedCheckboxes.length === 0) {
            alert("Please select at least one school.");
            return false;
        }

        if (selectedCheckboxes.length > maxSchools) {
            alert(`Please select a maximum of ${maxSchools} schools.`);
            return false;
        }
        
        // Validate numeric fields
        const numericFields = [
            { element: this.totalStudentsInput, name: "students per day" },
            { element: this.weeksInput, name: "weeks" },
            { element: this.hoursPerDayInput, name: "hours per day" },
            { element: this.costPerStudentInputEditable, name: "cost per student" },
            { element: this.maxSchoolsInput, name: "maximum schools" }
        ];

        for (const field of numericFields) {
            if (!this.validateInput(field.element)) {
                alert(`Please enter a valid value for ${field.name}.`);
                field.element.focus();
                return false;
            }
        }

        return true;
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new SchoolDataExplorer();
});
