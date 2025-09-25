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
        this.rfpTypeRadios = document.querySelectorAll('input[name="rfp_type"]');
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
        this.costPerSchoolInput = document.getElementById('cost-per-school-input');
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
            weeklyCost: document.getElementById('weekly-cost-for-ai-hidden'),
            costPerSchool: document.getElementById('cost-per-school-for-ai-hidden'),
            selectedSchoolsList: document.getElementById('selected-schools-list-hidden'),
            programStartDate: document.getElementById('program-start-date-hidden')
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
        this.rfpTypeRadios.forEach(radio => {
            radio.addEventListener('change', () => this.updateConstraints());
        });

        // School selection
        this.selectAllSchoolsCheckbox.addEventListener('change', () => this.handleSelectAllSchools());

        // Program configuration changes (all editable fields)
        this.totalStudentsInput.addEventListener('input', () => this.handleStudentsChange());
        this.weeksInput.addEventListener('input', () => this.handleWeeksChange());
        this.daysInput.addEventListener('change', () => this.updateAllCostsAndDetails());
        this.hoursPerDayInput.addEventListener('input', () => this.handleHoursChange());
        this.costPerStudentInputEditable.addEventListener('input', () => this.handleCostPerStudentChange());
        this.costPerStudentInputEditable.addEventListener('blur', () => this.formatCostPerStudentInput());
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
        // Check if this is the cost per student input (currency field)
        const isCurrencyField = input.id === 'cost-per-student-input-editable';

        let value, min, max;
        if (isCurrencyField) {
            value = this.parseCurrency(input.value);
            min = this.parseCurrency(input.min) || 0;
            max = this.parseCurrency(input.max) || Infinity;
        } else {
            value = parseFloat(input.value);
            min = parseFloat(input.min) || 0;
            max = parseFloat(input.max) || Infinity;
        }

        if (isNaN(value) || value < min || value > max) {
            const minDisplay = isCurrencyField ? this.formatCurrency(min) : min;
            const maxDisplay = isCurrencyField && max !== Infinity ? this.formatCurrency(max) : max;
            this.showValidationMessage(input, `Please enter a value between ${minDisplay} and ${maxDisplay}`);
            return false;
        }

        this.clearValidationMessage(input);
        return true;
    }

    updateConstraints() {
        // Update constraints display based on current values
        this.updateConstraintDisplay();

        // Update school selection constraints
        this.enforceMaxSchools();
    }

    updateConstraintDisplay() {
        const maxStudents = parseInt(this.totalStudentsInput.max) || this.CONSTANTS.MAX_STUDENTS_DEFAULT;
        const maxHours = parseInt(this.hoursPerDayInput.max) || this.CONSTANTS.MAX_HOURS_DEFAULT;
        const maxCostPerStudent = this.parseCurrency(this.costPerStudentInputEditable.max) || this.CONSTANTS.MAX_COST_PER_STUDENT_DEFAULT;
        const maxWeeks = parseInt(this.weeksInput.max) || this.CONSTANTS.MAX_WEEKS_DEFAULT;
        const maxSchools = parseInt(this.maxSchoolsInput.max) || this.CONSTANTS.MAX_SCHOOLS_DEFAULT;
        
        const currentCostPerStudent = this.parseCurrency(this.costPerStudentInputEditable.value) || 20;
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
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    }

    parseCurrency(value) {
        if (typeof value === 'number') {
            return value;
        }
        if (typeof value === 'string') {
            // Remove all non-numeric characters except decimal point and negative sign
            const cleaned = value.replace(/[^0-9.-]/g, '');
            const parsed = parseFloat(cleaned);
            return isNaN(parsed) ? 0 : parsed;
        }
        return 0;
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
        const value = this.parseCurrency(this.costPerStudentInputEditable.value);
        const max = this.parseCurrency(this.costPerStudentInputEditable.max) || this.CONSTANTS.MAX_COST_PER_STUDENT_DEFAULT;
        
        if (value > max) {
            this.costPerStudentInputEditable.value = this.formatCurrency(max);
            this.showValidationMessage(this.costPerStudentInputEditable, `Maximum ${this.formatCurrency(max)} per student allowed`);
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
        const costPerStudent = this.parseCurrency(this.costPerStudentInputEditable.value) || 0;
        const hoursPerDay = parseFloat(this.hoursPerDayInput.value) || 1;
        const costPerHour = costPerStudent / hoursPerDay;
        this.costPerHourInput.value = this.formatCurrency(costPerHour);
    }

    formatCostPerStudentInput() {
        const value = this.parseCurrency(this.costPerStudentInputEditable.value);
        if (value > 0) {
            this.costPerStudentInputEditable.value = this.formatCurrency(value);
            // Trigger calculation update after formatting
            this.updateAllCostsAndDetails();
        }
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
        const costPerStudentPerDay = this.parseCurrency(this.costPerStudentInputEditable.value) || 20;

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
        const costPerSchool = numSchoolsSelected > 0 ? totalProgramCost / numSchoolsSelected : 0;

        // Debug logging for troubleshooting
        console.log('🔢 Cost Calculation Update:', {
            'Schools Selected': numSchoolsSelected,
            'Students/Day': studentsPerDay,
            'Cost/Student/Day': `$${costPerStudentPerDay}`,
            'Days/Week': daysPerWeek,
            'Weeks': weeks,
            'Daily Cost': `$${dailyCost}`,
            'Weekly Cost': `$${weeklyCost}`,
            'Total Program Cost': `$${totalProgramCost}`,
            '💰 Cost Per School': `$${costPerSchool}`
        });

        // Update cost displays
        this.dailyCostInput.value = this.formatCurrency(dailyCost);
        this.weeklyCostInput.value = this.formatCurrency(weeklyCost);
        this.costPerSchoolInput.value = this.formatCurrency(costPerSchool);
        this.costProposalInput.value = this.formatCurrency(totalProgramCost);

        // Calculate program start date (first Monday of next month)
        const programStartDate = this.calculateProgramStartDate();

        // Get selected schools list
        const selectedSchools = Array.from(document.querySelectorAll('input[name="schoolname"]:checked'))
            .map(checkbox => JSON.parse(checkbox.dataset.schoolData)['School Name']);

        // Update program capacity
        this.updateProgramCapacity();

        // Update hidden inputs for backend submission
        this.hiddenInputs.totalStudents.value = studentsPerDay;
        this.hiddenInputs.costPerStudent.value = costPerStudentPerDay.toFixed(2);
        this.hiddenInputs.hoursPerDay.value = hoursPerDay;
        this.hiddenInputs.dailyCost.value = dailyCost.toFixed(2);
        this.hiddenInputs.weeklyCost.value = weeklyCost.toFixed(2);
        this.hiddenInputs.costPerSchool.value = costPerSchool.toFixed(2);
        this.hiddenInputs.selectedSchoolsList.value = JSON.stringify(selectedSchools);
        this.hiddenInputs.programStartDate.value = programStartDate;
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

    calculateProgramStartDate() {
        const now = new Date();
        const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);

        // Find the first Monday of next month
        const firstMonday = new Date(nextMonth);
        while (firstMonday.getDay() !== 1) { // 1 = Monday
            firstMonday.setDate(firstMonday.getDate() + 1);
        }

        // Format as YYYY-MM-DD
        return firstMonday.toISOString().split('T')[0];
    }

    formatProgramDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
}

// Tab Management
class TabManager {
    constructor() {
        this.setupTabs();
        this.loadProposalHistory();
    }

    setupTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');

                // Remove active class from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));

                // Add active class to clicked tab and corresponding content
                button.classList.add('active');
                document.getElementById(targetTab).classList.add('active');

                // Load history when switching to history tab
                if (targetTab === 'history') {
                    this.loadProposalHistory();
                }
            });
        });
    }

    async loadProposalHistory() {
        const historyContainer = document.getElementById('history-container');
        const historyCount = document.getElementById('history-count');

        try {
            // Show loading state
            historyContainer.innerHTML = `
                <div class="loading-history">
                    <div class="loader"></div>
                    <p>Loading proposal history...</p>
                </div>
            `;

            const response = await fetch('/api/proposal-history');
            if (!response.ok) {
                throw new Error('Failed to fetch history');
            }

            const data = await response.json();
            const proposals = data.proposals || [];

            // Update count
            historyCount.textContent = `${proposals.length} proposal(s) found`;

            if (proposals.length === 0) {
                historyContainer.innerHTML = `
                    <div class="no-history">
                        <span class="no-history-icon">📄</span>
                        <h3>No proposals found</h3>
                        <p>Create your first proposal using the "Create New Proposal" tab.</p>
                    </div>
                `;
                return;
            }

            // Build history list
            const historyHTML = proposals.map(proposal => {
                const date = new Date(proposal.created_date * 1000);
                const fileSize = this.formatFileSize(proposal.file_size);
                const formattedDate = date.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });

                // Determine file type and styling
                const isPDF = proposal.filename.endsWith('.pdf');
                const fileTypeIcon = isPDF ? '📄' : '📝';
                const fileTypeText = isPDF ? 'PDF' : 'DOCX';
                const fileTypeClass = isPDF ? 'file-type-pdf' : 'file-type-docx';
                const downloadButtonClass = isPDF ? 'download-history-btn-pdf' : 'download-history-btn-docx';

                return `
                    <div class="history-item">
                        <div class="history-info">
                            <div class="history-title">
                                <span class="file-type-badge ${fileTypeClass}">${fileTypeIcon} ${fileTypeText}</span>
                                ${proposal.district} - ${proposal.rfp_type}
                            </div>
                            <div class="history-meta">
                                <span>📅 ${formattedDate}</span>
                                <span>📁 ${fileSize}</span>
                            </div>
                        </div>
                        <div class="history-actions">
                            <a href="${proposal.download_url}"
                               class="download-history-btn ${downloadButtonClass}"
                               download="${proposal.filename}">
                                📥 Download ${fileTypeText}
                            </a>
                            <button onclick="deleteProposal('${proposal.filename}')"
                                    class="delete-history-btn">
                                🗑️ Delete
                            </button>
                        </div>
                    </div>
                `;
            }).join('');

            historyContainer.innerHTML = `<div class="history-list">${historyHTML}</div>`;

        } catch (error) {
            console.error('Error loading proposal history:', error);
            historyContainer.innerHTML = `
                <div class="no-history">
                    <span class="no-history-icon">⚠️</span>
                    <h3>Error loading history</h3>
                    <p>Please try refreshing the page or contact support if the problem persists.</p>
                </div>
            `;
            historyCount.textContent = 'Error loading';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }
}

// Global function for refresh button
function loadProposalHistory() {
    if (window.tabManager) {
        window.tabManager.loadProposalHistory();
    }
}

// Global function for deleting proposals
function deleteProposal(filename) {
    showConfirmationDialog(filename);
}

// Custom styled confirmation dialog
function showConfirmationDialog(filename) {
    // Create dialog overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';

    // Create dialog content
    const dialog = document.createElement('div');
    dialog.className = 'modal-dialog';

    dialog.innerHTML = `
        <div class="modal-header">
            <h3>🗑️ Confirm Delete</h3>
        </div>
        <div class="modal-body">
            <p>Are you sure you want to delete this proposal?</p>
            <div class="filename-display">${filename}</div>
            <p class="warning-text">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
            <button type="button" class="modal-btn modal-btn-cancel" onclick="closeConfirmationDialog()">
                Cancel
            </button>
            <button type="button" class="modal-btn modal-btn-delete" onclick="confirmDelete('${filename}')">
                Delete
            </button>
        </div>
    `;

    overlay.appendChild(dialog);
    document.body.appendChild(overlay);

    // Store reference for cleanup
    window.currentModal = overlay;

    // Focus on cancel button for accessibility
    setTimeout(() => {
        dialog.querySelector('.modal-btn-cancel').focus();
    }, 100);
}

function closeConfirmationDialog() {
    if (window.currentModal) {
        document.body.removeChild(window.currentModal);
        window.currentModal = null;
    }
}

async function confirmDelete(filename) {
    try {
        const response = await fetch('/api/proposal-delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ filename: filename })
        });

        if (!response.ok) {
            throw new Error('Failed to delete proposal');
        }

        await response.json();

        // Close the dialog
        closeConfirmationDialog();

        // Show success message briefly
        showNotification('Proposal deleted successfully', 'success');

        // Reload the history
        if (window.tabManager) {
            window.tabManager.loadProposalHistory();
        }

    } catch (error) {
        console.error('Error deleting proposal:', error);
        showNotification('Failed to delete proposal. Please try again.', 'error');
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new SchoolDataExplorer();
    window.tabManager = new TabManager();
});
