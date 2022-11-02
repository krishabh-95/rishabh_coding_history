import java.util.Scanner;
import java.util.ArrayList;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

/**
 * @author Rishabh K Iyer (ID: 103170582)
 * @version JDK 11.0.12
 * @date 15 October 2021
 * This is the main class of the application that contains all the options displayed to the user in the GUI
 * It allows the users to perform the following operations:-
 * Add a parking slot.
 * Delete a parking slot by slot ID (only if not occupied)
 * List all slots in a well-defined format along with all the required information.
 * Park a car into a slot (provide slot ID and car information).
 * Find a car by registration number and show the slot and the owner of the car.
 * Remove a car by registration number
 * Exit
 * It also lists all the parking slots in the UI and allows the user to view teh details of each slot by clicking on it
 */
public class Application
{
    private static JFrame frame;
    
    public static void main(String[] args)
    {        
        int staffSlots=-1, visitorSlots = -1;
        frame = new JFrame("Car Parking Registry");
        
        do
        {
            try
            {
                staffSlots = Integer.parseInt(JOptionPane.showInputDialog("Please enter the initial number of staff parking slots"));
            } catch(Exception ex)
            {
                //Unexpected error occurred
            }
            
            if(staffSlots<0)
            {
                JOptionPane.showMessageDialog(frame, "Please enter a positive number", "Invalid input", JOptionPane.ERROR_MESSAGE);
            }
            
            if(staffSlots>1300)
            {
                JOptionPane.showMessageDialog(frame, "The maximum number of staff slots possible is 1300", "Invalid input", JOptionPane.ERROR_MESSAGE);
            }
        } while(staffSlots<0 || staffSlots>1300);
        
        do
        {
            try
            {
                visitorSlots = Integer.parseInt(JOptionPane.showInputDialog("Please enter the initial number of visitor parking slots"));
            } catch(Exception ex)
            {
                //Unexpected error occurred
            }
            
            if(visitorSlots<0)
            {
                JOptionPane.showMessageDialog(frame, "Please enter a positive number", "Invalid input", JOptionPane.ERROR_MESSAGE);
            }
            
            if(visitorSlots>1300)
            {
                JOptionPane.showMessageDialog(frame, "The maximum number of visitor slots possible is 1300", "Invalid input", JOptionPane.ERROR_MESSAGE);
            }
        } while(visitorSlots<0 || visitorSlots>1300);
            
        try
        {
            ParkingSlot.addParkingSlots(staffSlots,'S');
            ParkingSlot.addParkingSlots(visitorSlots,'V');
            
            showHomeFrame();      
        } catch(Exception ex)
        {
            System.out.println("The following error has occurred.");
            System.out.println(ex);
        }
    }
    
    /**
     * This method displays the home page of the JFrame which is the main page of our application
     */
    private static void showHomeFrame() throws Exception
    {
            ArrayList<ParkingSlot> slotsList = CarPark.getParkingSlotsList();
             
            JSplitPane splitPane = new JSplitPane();
            
            //Panel for displaying the parking slots
            JPanel panel = new JPanel();
            
            for(int ind=0;ind<slotsList.size();ind++)
            {
                ParkingSlot ps = slotsList.get(ind);
                String slotId = ps.getSlotId();
                char slotType = ps.getSlotType();
                
                JButton button = new JButton(slotId);
                
                if(ps.getParkedCar() == null)
                {
                    if(slotType=='S')
                    {
                        button.setBackground(Color.CYAN);
                    }
                    else
                    {
                        button.setBackground(Color.YELLOW);                    
                    }
                }
                else
                {
                    if(slotType=='S')
                    {
                        button.setBackground(Color.GREEN);
                    }
                    else
                    {
                        button.setBackground(Color.ORANGE);
                    }
                }
                
                Font buttonFont=new Font(button.getFont().getName(),button.getFont().getStyle(),15);
                button.setFont(buttonFont);
                button.setSize(30, 30);
                
                button.addActionListener(new MainActionListener());
                
                panel.add(button);
            }
            
            int rootVal =(int)java.lang.Math.sqrt(slotsList.size());
            
            panel.setLayout(new GridLayout(rootVal,rootVal,10,10));
            
            JScrollPane slotsPane = new JScrollPane(panel);  
  
            slotsPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);  
            slotsPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);  
                      
            JPanel optionsPanel = new JPanel();
            JLabel label = new JLabel("Car Parking Options");
            label.setFont(new Font(label.getFont().getName(),label.getFont().getStyle(),20));
            label.setHorizontalAlignment(SwingConstants.CENTER);
            label.setVerticalAlignment(SwingConstants.CENTER);
            optionsPanel.add(label);
            
            JButton btn = new JButton("Add a parking slot");
            optionsPanel.add(btn); 
            btn.addActionListener(new MainActionListener());
            
            JButton btn2= new JButton("Delete a parking slot by slot ID (only if not occupied)");
            optionsPanel.add(btn2);
            btn2.addActionListener(new MainActionListener());
            
            JButton btn3= new JButton("List all the slots in the parking lot");
            optionsPanel.add(btn3);
            btn3.addActionListener(new MainActionListener());
            
            JButton btn4= new JButton("Park a car into a slot (provide slot ID and car information)");
            optionsPanel.add(btn4);
            btn4.addActionListener(new MainActionListener());
            
            JButton btn5= new JButton("Find a car by its registration number and show the slot and the owner of the car");
            optionsPanel.add(btn5);  
            btn5.addActionListener(new MainActionListener());
            
            JButton btn6= new JButton("Remove a car by registration number");
            optionsPanel.add(btn6);
            btn6.addActionListener(new MainActionListener());
            
            JButton btn7= new JButton("Exit");
            optionsPanel.add(btn7);
            btn7.addActionListener(new ActionListener() {
                 public void actionPerformed(ActionEvent e) {
                     System.exit(0);
                 }
            });
            
            CustomPanel key = new CustomPanel();
            optionsPanel.add(key);
            optionsPanel.setLayout(new GridLayout(9,1,10,10));
            
            splitPane.setOrientation(JSplitPane.HORIZONTAL_SPLIT);  
            splitPane.setDividerLocation(800);                    
            splitPane.setLeftComponent(slotsPane);                  
            splitPane.setRightComponent(optionsPanel);
            
            frame.getContentPane().add(splitPane);
            frame.setSize(1200,800);
            //frame.pack();
            frame.setVisible(true);     
    }
    
    /**
     * This method is used to add a parking slot from the user interface
     */
    private static void addParkingSlotFrame()
    {
        JFrame jframe = new JFrame("Adding a parking slot");
        
        try
        {
            JTextField slot = new JTextField("Please enter the slot ID (an uppercase letter followed by two digits)");
            slot.setBounds(10,30,400,20);
            jframe.add(slot);

            JLabel slotTypeLabel = new JLabel("Choose the type of parking slot");
            slotTypeLabel.setBounds(10,70,300,20);
            jframe.add(slotTypeLabel);

            JRadioButton rb1 = new JRadioButton("Staff");
            rb1.setBounds(10, 110, 200, 20);

            JRadioButton rb2 = new JRadioButton("Visitor");
            rb2.setBounds(10, 140, 200, 20);

            ButtonGroup bgrp=new ButtonGroup();    
            bgrp.add(rb1);
            bgrp.add(rb2);   
            jframe.add(slotTypeLabel);
            jframe.add(rb1);
            jframe.add(rb2);

            JButton btn =new JButton("Add");
            btn.setBounds(110,170,70,25);
            jframe.add(btn);
            
            jframe.setLayout(null);
            jframe.setSize(500,300);
            jframe.setVisible(true);
            
            btn.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e)
                {
                    String slotId = slot.getText().trim();    
    
                    boolean isValid=false;
                                          
                        //Checking if the slot ID is in the correct format
                        if(slotId!=null && slotId.length()==3)
                        {
                            char firstLetter= slotId.charAt(0);
                                            
                            if((int)firstLetter>=65 && (int)firstLetter<=90)
                            {                                                     
                                for(int index=0;index<2;index++)
                                {
                                    try
                                    {
                                        int num= new Integer(slotId.substring(1+index, 2+index));
                                        isValid= true;                               
                                    } catch(Exception exp)
                                    {
                                        //Incorrect format entered by the user
                                        isValid= false;
                                        break;
                                    }
                                }
                                                
                                if(isValid)
                                {
                                    boolean choiceSelected=false;
                                    
                                    if(rb1.isSelected())
                                    {
                                        choiceSelected=true;
                                        char slotType='S';
                                        ParkingSlot ps = new ParkingSlot(slotId, slotType, null);
                                        boolean op=false;
                                        
                                        try
                                        {
                                            op= CarPark.addSlot(ps); //Adding the parking slot to the existing list of slots 
                                        } catch(Exception exp)
                                        {
                                            //Unexpected error occurred
                                            jframe.dispose();
                                        }
                                        
                                        if(!op)
                                        {
                                            JOptionPane.showMessageDialog(jframe,
                                                "The slot ID for the slot that you are trying to add already exists. Please try again by entering a unique ID.",
                                                "Invalid input", JOptionPane.ERROR_MESSAGE);
                                            return;
                                        }

                                        JOptionPane.showMessageDialog(jframe, "The parking slot having ID "+slotId+" was added successfully.",
                                            "Operation successful", JOptionPane.INFORMATION_MESSAGE);
                                        jframe.dispose();   
                                        frame.getContentPane().removeAll();
                                        
                                        try
                                        {
                                            showHomeFrame();
                                        } catch(Exception ex)
                                        {
                                            //Unexpected error has occurred
                                        }
                                    }

                                    if(rb2.isSelected())
                                    {
                                        choiceSelected=true;
                                        char slotType='V';
                                        ParkingSlot ps = new ParkingSlot(slotId, slotType, null);
                                        boolean op=false;
                                        
                                        try
                                        {
                                            op= CarPark.addSlot(ps); //Adding the parking slot to the existing list of slots 
                                        } catch(Exception exp)
                                        {
                                            //Unexpected error occurred
                                            jframe.dispose();
                                        }

                                        if(!op)
                                        {
                                            JOptionPane.showMessageDialog(jframe,
                                                "The slot ID for the slot that you are trying to add already exists. Please try again by entering a unique ID.",
                                                "Invalid input", JOptionPane.ERROR_MESSAGE);
                                            return;
                                        }

                                        JOptionPane.showMessageDialog(jframe, "The parking slot having ID "+slotId+" was added successfully.",
                                            "Operation successful", JOptionPane.INFORMATION_MESSAGE);
                                        jframe.dispose(); 
                                        frame.getContentPane().removeAll();
                                        
                                        try
                                        {
                                            showHomeFrame();
                                        } catch(Exception ex)
                                        {
                                            //Unexpected error has occurred
                                        }
                                    }    
                                    
                                    if(!choiceSelected)
                                    {
                                        JOptionPane.showMessageDialog(jframe,
                                                "Please choose the type of parking slot.",
                                                "Invalid input", JOptionPane.ERROR_MESSAGE);
                                        return;
                                    }
                                                   
                                    return;
                                }
                            }
                        }
                                        
                        if(!isValid)
                        {
                            JOptionPane.showMessageDialog(jframe, "Please enter the ID in the correct format (an uppercase letter followed by two digits)",
                            "Invalid input", JOptionPane.ERROR_MESSAGE);
                        }  
                        return;
                }
             });
        } catch(Exception e)
        {
            //Unexpected issue occurred
            jframe.dispose();
        } 
    }
    
    /**
     * This method is used to delete a parking slot
     */
    private static void deleteParkingSlotFrame()
    {
        JFrame jframe = new JFrame("Deleting a parking slot");
        
        try
        {
            JTextField slot = new JTextField("Please enter the slot ID");
            slot.setBounds(10,30,200,20);
            jframe.add(slot);

            JButton btn =new JButton("Delete");
            btn.setBounds(70,60,80,25);
            jframe.add(btn);
            
            jframe.setLayout(null);
            jframe.setSize(300,200);
            jframe.setVisible(true);
            
            btn.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e)
                {                    
                    String slot_id = slot.getText().trim();
                    
                    try
                    {
                        ParkingSlot slot= CarPark.getSlot(slot_id);
                                        
                        if(slot!=null)
                        {
                            boolean op= CarPark.deleteSlot(slot);
                            
                            if(!op)
                            {
                                JOptionPane.showMessageDialog(jframe, "There is a car parked in this slot. So, it cannot be deleted.",
                                "Invalid input", JOptionPane.ERROR_MESSAGE);
                                jframe.dispose();
                                return;
                            }
                            
                            JOptionPane.showMessageDialog(jframe, "The slot having ID "+slot_id+" was deleted successfully.",
                                "Operation successful", JOptionPane.INFORMATION_MESSAGE);
                            
                            jframe.dispose(); 
                            frame.getContentPane().removeAll();
                            showHomeFrame();
                            return;
                        }
                        else
                        {
                            boolean isValid=false;
                            
                            //Checking if the slot ID is in the correct format
                            if(slot_id!=null && slot_id.length()==3)
                            {
                                char firstLetter= slot_id.charAt(0);
                                                
                                if((int)firstLetter>=65 && (int)firstLetter<=90)
                                {                                                     
                                    for(int index=0;index<2;index++)
                                    {
                                        try
                                        {
                                            int num= new Integer(slot_id.substring(1+index, 2+index));
                                            isValid= true;                               
                                        } catch(Exception exp)
                                        {
                                            //Incorrect format entered by the user
                                            isValid= false;
                                            break;
                                        }
                                    }                                                
                                }
                            }
                            
                            if(!isValid)
                            {
                                JOptionPane.showMessageDialog(jframe, "Please enter a valid slot ID (an uppercase letter followed by two digits)",
                                "Invalid input", JOptionPane.ERROR_MESSAGE);
                                return;
                            }
                            
                            JOptionPane.showMessageDialog(jframe, "There is no slot having the ID "+slot_id,
                            "Invalid input", JOptionPane.ERROR_MESSAGE);
                            jframe.dispose();
                        }
                        return;
                    } catch(Exception exp)
                    {
                        //Unexpected error occurred
                        jframe.dispose();
                        return;
                    }
                }
            });
        } catch(Exception ex)
        {
            //Unexpected error occurred
            jframe.dispose();
        }
    }
    
    /**
     * This method is used to park a car in one of the parking slots only if it is unoccupied 
     * and if the owner of the car falls under the category it is reserved for (staff member or visitor)
     */
    private static void parkCarInSlot()
    {
        JFrame jframe = new JFrame("Parking a car into a slot");
        
        try
        {
            JTextField slot = new JTextField("Enter the registration number of the car to be parked (an uppercase letter followed by a 4 digit number)");
            slot.setBounds(10,30,600,20);
            jframe.add(slot);
            
            JTextField slot2 = new JTextField("Enter the name of the owner");
            slot2.setBounds(10,60,400,20);
            jframe.add(slot2);
            
            JTextField slot3 = new JTextField("Enter the owner's phone number");
            slot3.setBounds(10,90,400,20);
            jframe.add(slot3);
            
            JLabel slotTypeLabel = new JLabel("Is the owner a staff member?");
            slotTypeLabel.setBounds(10,120,300,20);
            
            JRadioButton rb1 = new JRadioButton("Yes");
            rb1.setBounds(10, 150, 200, 20);

            JRadioButton rb2 = new JRadioButton("No");
            rb2.setBounds(10, 180, 200, 20);

            ButtonGroup bgrp=new ButtonGroup();    
            bgrp.add(rb1);
            bgrp.add(rb2);   
            jframe.add(slotTypeLabel);
            jframe.add(rb1);
            jframe.add(rb2);
            
            JTextField slot4 = new JTextField("Enter the slot ID of the slot where the car is to be parked");
            slot4.setBounds(10,210,400,20);
            jframe.add(slot4);
            
            JButton btn =new JButton("Add");
            btn.setBounds(250,250,70,25);
            jframe.add(btn);
                                
            jframe.setLayout(null);
            jframe.setSize(700,400);
            jframe.setVisible(true);
            
            btn.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e)
                {
                    try
                    {
                        String regNo = slot.getText().trim();
                        boolean regFormat=false;
                        boolean valid= false;
                        
                        if(regNo!=null && regNo.length()==5)
                        {
                            char firstLetter= regNo.charAt(0);
                            
                            if((int)firstLetter>=65 && (int)firstLetter<=90)
                            {
                                for(int index=0;index<4;index++)
                                {
                                    try
                                    {
                                        int num= new Integer(regNo.substring(1+index, 2+index));
                                        valid= true;                               
                                    } catch(Exception ex)
                                    {
                                        //Incorrect format entered by the user
                                        valid= false;
                                        break;
                                    }
                                } 
                                
                                if(valid)
                                {
                                    regFormat=true;
                                    String carOwner = slot2.getText().trim();
                                    
                                    if(carOwner==null || "".equals(carOwner))
                                    {
                                        JOptionPane.showMessageDialog(jframe,"The owner name cannot be empty. Please enter a valid name.",
                                           "Invalid input", JOptionPane.ERROR_MESSAGE );
                                        return;
                                    }
                                    
                                    String ownerPhoneNo = slot3.getText().trim();
                                    Long num = 0L;
                                    
                                    if(ownerPhoneNo==null || "".equals(ownerPhoneNo))
                                    {
                                       JOptionPane.showMessageDialog(jframe,"The owner's phone number cannot be empty. Please enter a valid number.",
                                           "Invalid input", JOptionPane.ERROR_MESSAGE );
                                       return; 
                                    }
                                    else
                                    {
                                        try
                                        {
                                            num = new Long(ownerPhoneNo);   
                                        } catch(Exception exp)
                                        {
                                            //Number format exception
                                            JOptionPane.showMessageDialog(jframe,"Please enter a valid phone number. It should not contain any special characters.",
                                            "Invalid input", JOptionPane.ERROR_MESSAGE );
                                            return;
                                        }
                                    }
                                    
                                    boolean staffSelection = false, isStaffMember= false;
                                    
                                    if(rb1.isSelected())
                                    {
                                        isStaffMember=true;
                                        staffSelection=true;
                                    }
                                    
                                    if(rb2.isSelected())
                                    {
                                        staffSelection=true;
                                    }
                                    
                                    if(!staffSelection)
                                    {
                                        JOptionPane.showMessageDialog(jframe,"Please select whether the owner is a staff member or not (Yes/No).",
                                            "Invalid input", JOptionPane.ERROR_MESSAGE );
                                        return;
                                    }
                                    
                                    Car newCar= new Car(regNo, carOwner, isStaffMember, num);
                                    
                                    String slot_Id = slot4.getText().trim();                                
                                    ParkingSlot parkingSlot= CarPark.getSlot(slot_Id);
                                    
                                    if(parkingSlot!=null)
                                    {
                                        //If this slot is occupied, we will give the user a chance to enter a different slot
                                        if(parkingSlot.getParkedCar()!=null)
                                        {
                                            int choice = JOptionPane.showConfirmDialog(jframe,
                                              "This slot is already occupied. Do you want to try again by entering another slot ID?",
                                              "Invalid input",
                                              JOptionPane.YES_NO_OPTION,
                                      JOptionPane.ERROR_MESSAGE);
                                  
                                        if(choice == JOptionPane.NO_OPTION)
                                    {
                                                jframe.dispose();   
                                            }
                                        
                                            return;
                                        }
                                        else if((parkingSlot.getSlotType()=='V' && newCar.isOwnerStaffMember()) || (parkingSlot.getSlotType()=='S' && !newCar.isOwnerStaffMember()))
                                        {
                                            //If the owner of the car doesn't fall under the category the slot is reserved for, this block will get invoked
                                            int choice = JOptionPane.showConfirmDialog(jframe,
                                              "This slot is reserved for "+(parkingSlot.getSlotType()=='V'?"visitors":"staff members")+"."+
                                              "Do you want to try again by entering another ID?",
                                              "Invalid input",
                                              JOptionPane.YES_NO_OPTION,
                                  JOptionPane.ERROR_MESSAGE);
                                  
                                    if(choice == JOptionPane.NO_OPTION)
                                    {
                                                    jframe.dispose();   
                                                }
                                        
                                            return;
                                        }
                                        else
                                        {
                                            boolean op = parkingSlot.addCar(newCar);
                                            
                                            if(!op)
                                            {
                                                
                                                JOptionPane.showMessageDialog(jframe,"This car is already parked in the slot "+
                                                CarPark.getSlotFromRegistrationNo(newCar.getRegistrationNo()).getSlotId()+". Please remove it from this slot before parking it elsewhere.",
                                                "Invalid input", JOptionPane.ERROR_MESSAGE);
                                                return;
                                            }
                                            
                                            JOptionPane.showMessageDialog(jframe, "The car was added to this slot successfully.",
                                            "Operation successful", JOptionPane.INFORMATION_MESSAGE);
                                            jframe.dispose();   
                                            frame.getContentPane().removeAll();
                                            showHomeFrame();
                                            return;
                                        }
                                
                                    }
                                    else
                                    {
                                        int choice = JOptionPane.showConfirmDialog(jframe,
                                              "There is no slot having the given slot ID. Do you want to try again by entering another ID?",
                                              "Invalid input",
                                              JOptionPane.YES_NO_OPTION,
                                      JOptionPane.ERROR_MESSAGE);
                                  
                            if (choice == JOptionPane.NO_OPTION)
                            {
                                           jframe.dispose();   
                                        }
                                        
                                        return;
                                    }
                                    
                                }    
                            }
                        }
                        
                        if(!regFormat)
                        {
                            //Registration number format incorrect
                            JOptionPane.showMessageDialog(jframe,"Please enter the registration number in the correct format (an uppercase letter followed by a four digit number)",
                                           "Invalid input", JOptionPane.ERROR_MESSAGE );
                            return;
                        }
                    } catch(Exception exp)
                    {
                        //Unexpected error
                        jframe.dispose();
                    }
                }
            });
            
        } catch(Exception exp)
        {
            //Unexpected error  
            jframe.dispose();
        }
    }
    
    /**
     * @param slotId : The slot ID of the parking slot whose details need to be viewed
     */
    private static void showSlotDetails(String slot_id)
    {
        JFrame jframe = new JFrame("Parking Slot Details");
        
        try
        {
                    ParkingSlot slot = CarPark.getSlot(slot_id);
                    String slotType = (slot.getSlotType()=='S'?"Staff Parking":"Visitor Parking");
                    String carStr="";  
                    
                    if(slot.getParkedCar()==null)
                    {
                       carStr="There is no car in this slot.";
                    }
                    else
                    {                       
                       Car car = slot.getParkedCar();
                       carStr="The car parked in this slot has registration number "+car.getRegistrationNo()+".<br> Its owner is "+car.getOwnerName()+".<br>The owner's phone number is "+car.getOwnerPhoneNo()+".";
                    }
                    
                    JLabel label = new JLabel("<html>Slot ID: "+slot_id+"<br>Slot Type: "+slotType+"<br>"+carStr+"</html>");
                    label.setFont(new Font(label.getFont().getName(),label.getFont().getStyle(),15)); 
                    
                    if(slot.getParkedCar()==null)
                    {
                       if("Staff Parking".equals(slotType))
                       {
                            label.setBackground(Color.CYAN);
                       }
                       else
                       {
                            label.setBackground(Color.YELLOW);
                       }
                       label.setSize(new Dimension(500, 180));
                    }
                    else
                    {
                       if("Staff Parking".equals(slotType))
                       {
                            label.setBackground(Color.GREEN);
                       }
                       else
                       {
                            label.setBackground(Color.ORANGE);
                       } 
                       label.setSize(new Dimension(500, 320));
                    }
                    
                    label.setOpaque(true);
                    jframe.getContentPane().add(label);
                    
                    jframe.setLayout(null);
                    jframe.setSize(500,300);
                    jframe.setVisible(true);
        } catch(Exception ex)
        {
            //Unexpected error
            jframe.dispose();
        }
    }
    
    /**
     * This method is used to find a car using its registration number
     */
    private static void findCarUsingRegNo() 
    {
        JFrame jframe = new JFrame("Finding a car using the registration number");
        
        try
        {
            JTextField slot = new JTextField("Please enter the registration number of the car");
            slot.setBounds(10,30,250,20);
            jframe.add(slot);
            
            JButton btn = new JButton("Search");
            btn.setBounds(90,60,80,25);
            jframe.add(btn);
            
            jframe.setSize(600,400);
            jframe.setLayout(null);
            jframe.setVisible(true);
            
            btn.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e)
                {
                    try
                    {
                        String registrationNo = slot.getText().trim();
                        ParkingSlot pSlot = CarPark.getSlotFromRegistrationNo(registrationNo);
                        
                        if(pSlot!=null)
                        {
                            JOptionPane.showMessageDialog(jframe, "This car is parked in slot "+pSlot.getSlotId()+
                                            ". Its owner is "+pSlot.getParkedCar().getOwnerName()+" and the owner's phone number is "+pSlot.getParkedCar().getOwnerPhoneNo()+".",
                                            "Operation successful", JOptionPane.INFORMATION_MESSAGE);
                            jframe.dispose();   
                            return;
                        }
                        else
                        {
                            boolean valid = false;
                            
                            //Checking if the entered registration number has the correct format
                            if(registrationNo!=null && registrationNo.length()==5)
                            {
                                char firstLetter= registrationNo.charAt(0);
                                
                                if((int)firstLetter>=65 && (int)firstLetter<=90)
                                {
                                    for(int index=0;index<4;index++)
                                    {
                                        try
                                        {
                                            int num= new Integer(registrationNo.substring(1+index, 2+index));
                                            valid= true;                               
                                        } catch(Exception ex)
                                        {
                                            //Incorrect format entered by the user
                                            valid= false;
                                            break;
                                        }
                                    } 
                                }
                            }
                            
                            if(!valid)
                            {
                                JOptionPane.showMessageDialog(jframe,"Please enter a valid registration number (an uppercase letter followed by a 4 digit number).",
                                "Invalid input", JOptionPane.ERROR_MESSAGE );
                            }
                            else
                            {
                                int choice = JOptionPane.showConfirmDialog(jframe,
                                              "There is no car with the given registration number. Do you want to try again?",
                                              "Invalid input",
                                              JOptionPane.YES_NO_OPTION,
                                      JOptionPane.ERROR_MESSAGE);
                                      
                        if(choice == JOptionPane.NO_OPTION)
                        {
                            jframe.dispose();
                                }
                                return;
                            }
                        }  
                    } catch(Exception exp)
                    {
                        //Unexpected error
                        jframe.dispose();
                    }
                }
            });              
                
        } catch(Exception exp)
        {
            //Unexpected error
            jframe.dispose();
        }
    }
    
    /**
     * This method is used to remove a car from a slot using its registration number
     */
    private static void removeCarUsingRegNo()
    {
        JFrame jframe = new JFrame("Removing a car using its registration number");
        
        try
        {
            JTextField slot = new JTextField("Please enter the registration number of the car");
            slot.setBounds(10,30,300,20);
            jframe.add(slot);

            JButton btn =new JButton("Delete");
            btn.setBounds(80,60,80,25);
            jframe.add(btn);
            
            jframe.setLayout(null);
            jframe.setSize(300,200);
            jframe.setVisible(true);
            
            btn.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e)
                {
                    try
                    {
                        String reg_No= slot.getText().trim();
                        ParkingSlot parkSlot = CarPark.getSlotFromRegistrationNo(reg_No);
                                        
                        if(parkSlot!=null)
                        {
                            parkSlot.removeCar();
                            JOptionPane.showMessageDialog(jframe, "The car having registration number "+reg_No+" was removed from the slot "+parkSlot.getSlotId(),
                                            "Operation successful", JOptionPane.INFORMATION_MESSAGE);
                            jframe.dispose();
                            frame.getContentPane().removeAll();
                            showHomeFrame();
                            return;
                        }
                        else
                        {
                            boolean valid = false;
                            
                            //Checking if the entered registration number has the correct format
                            if(reg_No!=null && reg_No.length()==5)
                            {
                                char firstLetter= reg_No.charAt(0);
                                
                                if((int)firstLetter>=65 && (int)firstLetter<=90)
                                {
                                    for(int index=0;index<4;index++)
                                    {
                                        try
                                        {
                                            int num= new Integer(reg_No.substring(1+index, 2+index));
                                            valid= true;                               
                                        } catch(Exception ex)
                                        {
                                            //Incorrect format entered by the user
                                            valid= false;
                                            break;
                                        }
                                    } 
                                }
                            }
                            
                            if(!valid)
                            {
                                JOptionPane.showMessageDialog(jframe,"Please enter a valid registration number (an uppercase letter followed by a 4 digit number).",
                                "Invalid input", JOptionPane.ERROR_MESSAGE );
                                return;
                            }
                            else
                            {
                                int choice = JOptionPane.showConfirmDialog(jframe,
                                              "There is no car with the given registration number. Do you want to try again?",
                                              "Invalid input",
                                              JOptionPane.YES_NO_OPTION,
                                      JOptionPane.ERROR_MESSAGE);
                                      
                        if(choice == JOptionPane.NO_OPTION)
                        {
                            jframe.dispose();
                                }
                                return;
                            }
                        }
                    } catch(Exception ex)
                    {
                        //Unexpected error occurred
                        jframe.dispose();
                    }
                }
            });
            
        } catch(Exception ex)
        {
            //Unexpected error occurred
            jframe.dispose();
        }      
    }
    
    //This is the listener class that is invoked whenever a button is clicked in the main frame
    static class MainActionListener implements ActionListener
    {
        public void actionPerformed(ActionEvent e)
        {
            if("Add a parking slot".equals(e.getActionCommand()))
            {
                addParkingSlotFrame();
            }
            else if("Delete a parking slot by slot ID (only if not occupied)".equals(e.getActionCommand()))
            {
                deleteParkingSlotFrame();
            }
            else if("List all the slots in the parking lot".equals(e.getActionCommand()))
            {
                CarPark.getParkingSlots();
            }
            else if("Park a car into a slot (provide slot ID and car information)".equals(e.getActionCommand()))
            {
                parkCarInSlot();
            }
            else if("Find a car by its registration number and show the slot and the owner of the car".equals(e.getActionCommand()))
            {
                findCarUsingRegNo();
            }
            else if("Remove a car by registration number".equals(e.getActionCommand()))
            {
                removeCarUsingRegNo();
            }
            else
            {
                //One of the parking slots was clicked
                showSlotDetails(e.getActionCommand());
            }
        }
    }
}

/** 
 * This is a custom class used to modify the default graphics options in the JPanel
 * It is used to diaplay the colour code to indicate which colour represents which type of parking slot in the main JFrame
 */
class CustomPanel extends JPanel {
  public void paint(Graphics gr) {
    gr.setFont(new Font(gr.getFont().getName(),Font.BOLD,gr.getFont().getSize()));
    gr.setColor(Color.CYAN);
    gr.fillRect(5,0,190,25);
    gr.setColor(Color.BLACK);
    gr.drawString("Unoccupied staff parking slots",10,15);
    gr.setColor(Color.YELLOW);
    gr.fillRect(5,30,190,25);
    gr.setColor(Color.BLACK);
    gr.drawString("Unoccupied visitor parking slots",10,45);
    gr.setColor(Color.GREEN);
    gr.fillRect(200,0,190,25);
    gr.setColor(Color.BLACK);
    gr.drawString("Occupied staff parking slots",205,15);
    gr.setColor(Color.ORANGE);
    gr.fillRect(200,30,190,25);
    gr.setColor(Color.BLACK);
    gr.drawString("Occupied visitor parking slots",205,45);
  }
}
